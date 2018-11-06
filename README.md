# AttrDict

AttrDict is an MIT-licensed library that provides mapping objects that allow
their elements to be accessed both as keys and as attributes:

```
> from attrdict import AttrDict
> a = AttrDict({'foo': 'bar'})
> a.foo
'bar'
> a['foo']
'bar'
```

Attribute access makes it easy to create convenient, hierarchical settings
objects:
```
with open('settings.yaml') as fileobj:
	settings = AttrDict(yaml.safe_load(fileobj))

cursor = connect(**settings.db.credentials).cursor()

cursor.execute("SELECT column FROM table;")
```

## Installation
This is a fork of the original, not available on PyPi so you will have to install as a git source using `pip` or `pipenv`. It can also be installed by running `python setup.py install`.

The original AttrDict is available on PyPi, so it can be install directly using:

```
$ pip install attrdict
```

## Basic Usage
AttrDict comes with three different classes, `AttrMap`, `AttrDict`, and `AttrDefault`. They are all fairly similar, as they all are MutableMappings (read: dictionaries) that allow creating, accessing, and deleting key-value pairs as attributes.

### Valid Names
Any key can be used as an attribute as long as:

1. The key represents a valid attribute (i.e., it is a string comprised only of
   alphanumeric characters and underscores that doesn't start with a number)
2. The key represents a public attribute (i.e., it doesn't start with an
   underscore). This is done (in part) so that implementation changes between
   minor and micro versions don't force major version changes.
3. The key does not shadow a class attribute (e.g., get).


### Attributes vs. Keys
There is a minor difference between accessing a value as an attribute vs.  accessing it as a key, is that when a dict is accessed as an attribute, it will automatically be converted to an Attr object. This allows you to recursively access keys:

```
> attr = AttrDict({'foo': {'bar': 'baz'}})
> attr.foo.bar
'baz'
```

Relatedly, by default, sequence types that aren't `bytes`, `str`, or `unicode` (e.g., lists, tuples) will automatically be converted to tuples, with any mappings converted to Attrs:

```
> attr = AttrDict({'foo': [{'bar': 'baz'}, {'bar': 'qux'}]})
> for sub_attr in attr.foo:
>     print(subattr.foo)
'baz'
'qux'
```

To get this recursive functionality for keys that cannot be used as attributes,
you can replicate the behavior by calling the Attr object:

```
> attr = AttrDict({1: {'two': 3}})
> attr(1).two
3
```

### Classes
AttrDict comes with three different objects, `AttrMap`, `AttrDict`, and `AttrDefault`.

#### AttrMap
The most basic implementation. Use this if you want to limit the number of invalid keys, or otherwise cannot use `AttrDict`

#### AttrDict
An Attr object that subclasses `dict`. You should be able to use this absolutely anywhere you can use a `dict`. While this is probably the class you want to use, there are a few caveats that follow from this being a `dict` under the hood.

The `copy` method (which returns a shallow copy of the mapping) returns a `dict` instead of an `AttrDict`.

Recursive attribute access results in a shallow copy, so recursive assignment will fail (as you will be writing to a copy of that dictionary):

```
> attr = AttrDict('foo': {})
> attr.foo.bar = 'baz'
> attr.foo
{}
```

Assignment as keys will still work:

```
> attr = AttrDict('foo': {})
> attr['foo']['bar'] = 'baz'
> attr.foo
{'bar': 'baz'}
```

If either of these caveats are deal-breakers, or you don't need your object to
be a `dict`, consider using `AttrMap` instead.

#### AttrDefault
At Attr object that behaves like a `defaultdict`. This allows on-the-fly, automatic key creation:

```
> attr = AttrDefault(int, {})
> attr.foo += 1
> attr.foo
1
```

AttrDefault also has a `pass_key` option that passes the supplied key to the `default_factory`:

```
> attr = AttrDefault(sorted, {}, pass_key=True)
> attr.banana
['a', 'a', 'a', 'b', 'n', 'n']
```

### Merging
All three Attr classes can be merged with eachother or other Mappings using the `+` operator. For conflicting keys, the right dict's value will be preferred, but in the case of two dictionary values, they will be recursively merged:

```
> a = {'foo': 'bar', 'alpha': {'beta': 'a', 'a': 'a'}}
> b = {'lorem': 'ipsum', 'alpha': {'bravo': 'b', 'a': 'b'}}
> AttrDict(a) + b
{'foo': 'bar', 'lorem': 'ipsum', 'alpha': {'beta': 'a', 'bravo': 'b', 'a': 'b'}}
```

NOTE: AttrDict's add is not commutative, `a + b != b + a`:

```
> a = {'foo': 'bar', 'alpha': {'beta': 'b', 'a': 0}}
> b = {'lorem': 'ipsum', 'alpha': {'bravo': 'b', 'a': 1}}
> b + AttrDict(a)
{'foo': 'bar', 'lorem': 'ipsum', 'alpha': {'beta': 'a', 'bravo': 'b', 'a': }}
```

### Sequences
By default, items in non-string Sequences (e.g. lists, tuples) will be converted to AttrDicts:

```
> adict = AttrDict({'list': [{'value': 1}, {'value': 2}]})
> for element in adict.list:
>     element.value
1
2
```

This will not occur if you access the AttrDict as a dictionary:

```
> adict = AttrDict({'list': [{'value': 1}, {'value': 2}]})
> for element in adict['list']:
>     isinstance(element, AttrDict)
False
False
```

To disable this behavior globally, pass the attribute `recursive=False` to the constructor:

```
> adict = AttrDict({'list': [{'value': 1}, {'value': 2}]}, recursive=False)
> for element in adict.list:
>     isinstance(element, AttrDict)
False
False
```

When merging an AttrDict with another mapping, this behavior will be disabled if at least one of the merged items is an AttrDict that has set `recursive` to `False`.

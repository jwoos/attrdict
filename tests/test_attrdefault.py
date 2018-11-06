"""
Tests for the AttrDefault class.
"""
from nose.tools import assert_equals, assert_raises


def test_method_missing():
    """
    default values for AttrDefault
    """
    from attrdict.default import AttrDefault

    default_none = AttrDefault()
    default_list = AttrDefault(list, sequence_type=None)
    default_double = AttrDefault(lambda value: value * 2, pass_key=True)

    assert_raises(AttributeError, lambda: default_none.foo)
    assert_raises(KeyError, lambda: default_none['foo'])
    assert_equals(default_none, {})

    assert_equals(default_list.foo, [])
    assert_equals(default_list['bar'], [])
    assert_equals(default_list, {'foo': [], 'bar': []})

    assert_equals(default_double.foo, 'foofoo')
    assert_equals(default_double['bar'], 'barbar')
    assert_equals(default_double, {'foo': 'foofoo', 'bar': 'barbar'})


def test_repr():
    """
    repr(AttrDefault)
    """
    from attrdict.default import AttrDefault

    assert_equals(repr(AttrDefault(None)), "AttrDefault(None, False, {})")

    assert_equals(
        repr(AttrDefault(list)),
        'class'.join(("AttrDefault(<", " 'list'>, False, {})"))
    )

    assert_equals(
        repr(AttrDefault(list, {'foo': 'bar'}, pass_key=True)),
        'class'.join(
            ("AttrDefault(<", " 'list'>, True, {'foo': 'bar'})")
        )
    )

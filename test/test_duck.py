import pytest

from duckt import Duck, DuckGet, DuckCall


class Obj:
    def __init__(self, val):
        self.some_property = val

    @property
    def prop(self):
        return self.some_property + 1

    @property
    def prop2(self):
        return self.prop + 10

    def foo(self):
        return self.prop

    def bar(self, some_arg1, some_arg2):
        return some_arg1 - some_arg2

    def baz(self, arg, *args, **kwargs):
        return str() + str(args) + str(kwargs)

    def __call__(self, argument1, *, argument2):
        return (argument1 + argument2) * 3


@pytest.fixture
def duck_obj():
    obj = Obj(42)
    return Duck(obj), obj


@pytest.mark.parametrize(
    "attrs, expected",
    [
        (
            [
                "non_existent",
                "another_non_existent",
                "try_again",
                "prop",
                "prop2",
                "this_should_not_be_even_tried",
            ],
            "prop",
        ),
        (["foo", "prop", "some_property"], "foo"),
        (["some_property", "prop2", "prop"], "some_property"),
    ],
)
def test_duck_attr(attrs, expected):
    """
    Should extract the first attribute present in obj
    """
    obj = Obj(42)
    duck = Duck(obj)
    assert duck.attr(*attrs) == getattr(obj, expected)


def test_duck_attr_default():
    """
    Should return default value when none of the attributes is found
    """
    obj = Obj(42)
    duck = Duck(obj)
    assert duck.attr("bad_property", "nope", default=12345426) == 12345426


def test_duck_attr_raise():
    """
    Should raise AttributeError when none of the attributes is found and
    no default value given
    """
    obj = Obj(42)
    duck = Duck(obj)
    with pytest.raises(AttributeError):
        duck.attr("bad_property", "nope")


def test_duck_attr_call():
    """
    Should traverse the attributes and try to call them with the given
    arguments, then return the result of the first successful call.
    """
    obj = Obj(42)
    duck = Duck(obj)
    duck_calls = [
        DuckCall(*p)
        for p in [
            ["foo"],
            ["bar", [3, 2]],
            ["baz", ["hello", "world"], {"some_arg": 419}],
        ]
    ]
    assert duck.attr_call(*duck_calls) == obj.foo()

    duck_calls = [
        DuckCall(*p)
        for p in [
            ["non_existent_method_without_arguments"],
            ["non_existent_method_with_args", [1, 2, 3]],
            ["baz", ["hello", "world"], {"some_arg": 419}],
            ["foo"],
            ["bar", [3, 2]],
        ]
    ]
    assert duck.attr_call(*duck_calls) == obj.baz("hello", "world", some_arg=419)


def test_duck_attr_call_fallback_property(duck_obj):
    """
    If an argument is a string, attr_call interprets it a name of the property
    to be returned.
    """
    obj = Obj(42)
    duck = Duck(obj)
    assert duck.attr_call(DuckCall("non_existent"), "prop") == obj.prop


def test_duck_attr_call_raise():
    """
    Should raise AttributeError if attribute is not present
    and TypeError if the signature of the method is not compatible with
    the arguments.
    """
    obj = Obj(42)
    duck = Duck(obj)
    with pytest.raises(AttributeError):
        assert duck.attr_call(DuckCall("non_existent"))

    # OK method, bad signature
    with pytest.raises(TypeError):
        assert duck.attr_call(DuckCall("foo", ["bad", "arguments"]))


def test_duck_call():
    """
    Should return the result of the first successful call the callable
    object.
    """
    obj = Obj(42)
    duck = Duck(obj)
    assert duck.call(
        [["foo"]], [], [["hello1", "world1"]], [["hello"], {"argument2": "world"}]
    ) == obj("hello", argument2="world")


def test_duck_noargs_call():
    """
    Should return the result of the first successful call the callable
    object.
    """

    def some_func():
        return "hello!"

    duck = Duck(some_func)
    assert (
        duck.call(
            [["foo"]], [], [["hello1", "world1"]], [["hello"], {"argument2": "world"}]
        )
        == "hello!"
    )


def test_duck_call_default():
    """
    Should return default value.
    """
    obj = Obj(42)
    duck = Duck(obj)
    assert duck.call([["bad", "arguments"]], default=1234) == 1234


def test_duck_call_raise():
    """
    Should raise TypeError
    """
    obj = Obj(42)
    duck = Duck(obj)
    with pytest.raises(TypeError):
        duck.call([["bad", "arguments"]])


def test_duck_get():
    """
    Should return propery value
    """
    obj = Obj(42)
    duck = Duck(obj)
    assert duck.attr_call(DuckGet("prop")) == obj.prop

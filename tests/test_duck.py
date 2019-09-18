import pytest

from duck import Duck, DuckGet, DuckCall


class Ducked:
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
    obj = Ducked(42)
    return Duck(obj), obj


attrs1 = (
    [
        "non_existent",
        "another_non_existent",
        "try_again",
        "prop",
        "prop2",
        "this_should_not_be_even_tried",
    ],
    "prop",
)
attrs2 = (["foo", "prop", "some_property"], "foo")
attrs3 = (["some_property", "prop2", "prop"], "some_property")


@pytest.mark.parametrize("attrs, expected", [attrs1, attrs2, attrs3])
def test_duck_attr(duck_obj, attrs, expected):
    duck, obj = duck_obj
    assert duck.attr(*attrs) == getattr(obj, expected)


@pytest.mark.parametrize("default", [1234, "string", {"a": 1}])
def test_duck_attr_default(duck_obj, default):
    duck, obj = duck_obj
    assert duck.attr("bad_property", "nope", default=default) == default


def test_duck_attr_raise(duck_obj):
    duck, obj = duck_obj
    with pytest.raises(AttributeError):
        duck.attr("bad_property", "nope")


method_calls = [
    [
        [["foo"], ["bar", [3, 2]], ["baz", ["hello", "world"], {"some_arg": 419}]],
        # expected
        ["foo"],
    ],
    [
        [
            ["non_existent_method_without_arguments"],
            ["non_existent_method_with_args", [1, 2, 3]],
            ["baz", ["hello", "world"], {"some_arg": 419}],
            ["foo"],
            ["bar", [3, 2]],
        ],
        # expected
        ["baz", ["hello", "world"], {"some_arg": 419}],
    ],
]


@pytest.mark.parametrize("contexts", method_calls)
def test_duck_attr_call(duck_obj, contexts):
    duck, obj = duck_obj
    contexts, expected = contexts
    duck_calls = [DuckCall(*ctx) for ctx in contexts]
    assert duck.attr_call(*duck_calls) == DuckCall(*expected)(obj)


def test_duck_attr_call_str(duck_obj):
    duck, obj = duck_obj
    assert duck.attr_call(DuckCall("non_existent"), "prop") == obj.prop


def test_duck_attr_call_raise(duck_obj):
    duck, obj = duck_obj
    with pytest.raises(AttributeError):
        assert duck.attr_call(DuckCall("non_existent"))

    # OK method, bad signature
    with pytest.raises(TypeError):
        assert duck.attr_call(DuckCall("foo", ["bad", "arguments"]))


def test_duck_call(duck_obj):
    duck, obj = duck_obj
    assert duck(
        [["foo"]], [], [["hello1", "world1"]], [["hello"], {"argument2": "world"}]
    ) == obj("hello", argument2="world")


@pytest.mark.parametrize("default", [1234, "string", {"a": 1}])
def test_duck_call_default(duck_obj, default):
    duck, obj = duck_obj
    assert duck([["bad", "arguments"]], default=default) == default


def test_duck_call_raise(duck_obj):
    duck, obj = duck_obj
    with pytest.raises(TypeError):
        duck([["bad", "arguments"]])

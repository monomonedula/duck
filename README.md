# duck
A small Python package facilitating duck typing through attribute traverse utilities

This replaces try/except chains when trying to call different methods:
```python
noise = Duck(creature).attr_call(
    DuckCall("make_sound", ["woof"]), # tries to call creature.make_sound("woof")
    DuckCall("make_sound", ["buzz", 100]), # tries to call creature.buzz("buzz", 100)
    DuckCall("bark"), # creature.bark()
    DuckCall("roar"), # creature.roar()
    DuckCall("speak", ["Hello "], {"times": 3}) # creature.speak("Hello ", times=3)
) # returns the output of the first successfull call

print(noise)
```
DuckCall class is fully replacable here with any custom callable accepting single argument. This argument is the Duck-wrapped object, so you can implement custom attribute extracting and/or calling behavior here. AttributeErrors and TypeErrors thrown from this callable is handled by the Duck object.


Simplified interface for property extraction:
```python
name = Duck(some_person).attr('first_name', 'name', 'full_name')
# name now is equal to the first present attribute
# otherwise AttributeError is thrown
```

You may also use Duck as wrapper to a callable:
```python
duck = Duck(some_callable)
duck(
    ["hello", "world"], # some_callable("hello", "world")
    ["hello world"],    # some_callable("hello world")
    [[], {"hello": "world"}]  # some_callable(hello="world")
)

```
That's it.

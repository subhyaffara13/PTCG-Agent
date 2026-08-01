
def register_data_type(type_: T, /) -> T:
  """Registers a type as pytree data type recognized by Object.

  Custom types registered as data will be automatically recognized
  as data attributes when assigned to an Object attribute. This means
  that values of this type do not need to be wrapped in `nnx.data(...)`
  for Object to mark the attribute its being assigned to as data.

  Example::

    from flax import nnx
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class MyType:
      value: int

    nnx.register_data_type(MyType)

    class Foo(nnx.Pytree):
      def __init__(self, a):
        self.a = MyType(a)  # Automatically registered as data
        self.b = "hello"     # str not registered as data

    foo = Foo(42)

    assert nnx.is_data(foo.a)  # True
    assert jax.tree.leaves(foo) == [MyType(value=42)]

  Can also be used as a decorator::

    @nnx.register_data_type
    @dataclass(frozen=True)
    class MyType:
      value: int
  """
  DATA_REGISTRY.add(type_)
  return type_


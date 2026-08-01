
def mappable_dataclass(cls):
  """Exposes dataclass as ``collections.abc.Mapping`` descendent.

  Allows to traverse dataclasses in methods from `dm-tree` library.

  NOTE: changes dataclasses constructor to dict-type
  (i.e. positional args aren't supported; however can use generators/iterables).

  Args:
    cls: A dataclass to mutate.

  Returns:
    Mutated dataclass implementing ``collections.abc.Mapping`` interface.
  """
  if not dataclasses.is_dataclass(cls):
    raise ValueError(f"Expected dataclass, got {cls} (change wrappers order?).")

  # Define methods for compatibility with `collections.abc.Mapping`.
  setattr(cls, "__getitem__", lambda self, x: self.__dict__[x])
  setattr(cls, "__len__", lambda self: len(self.__dict__))
  setattr(cls, "__iter__", lambda self: iter(self.__dict__))
  # Override the default `collections.abc.Mapping` method implementation for
  # cleaner visualization. Without this change x.keys() shows the full repr(x)
  # instead of only the dict_keys present. The same goes for values and items.
  setattr(cls, "keys", lambda self: self.__dict__.keys())
  setattr(cls, "values", lambda self: self.__dict__.values())
  setattr(cls, "items", lambda self: self.__dict__.items())

  # Update constructor.
  orig_init = cls.__init__
  all_fields = set(f.name for f in cls.__dataclass_fields__.values())
  init_fields = [f.name for f in cls.__dataclass_fields__.values() if f.init]

  @functools.wraps(orig_init)
  def new_init(self, *orig_args, **orig_kwargs):
    if (orig_args and orig_kwargs) or len(orig_args) > 1:
      raise ValueError(
          "Mappable dataclass constructor doesn't support positional args."
          "(it has the same constructor as python dict)")
    all_kwargs = dict(*orig_args, **orig_kwargs)
    unknown_kwargs = set(all_kwargs.keys()) - all_fields
    if unknown_kwargs:
      raise ValueError(f"__init__() got unexpected kwargs: {unknown_kwargs}.")

    # Pass only arguments corresponding to fields with `init=True`.
    valid_kwargs = {k: v for k, v in all_kwargs.items() if k in init_fields}
    orig_init(self, **valid_kwargs)

  cls.__init__ = new_init

  # Update base class to derive from Mapping
  dct = dict(cls.__dict__)
  if "__dict__" in dct:
    dct.pop("__dict__")  # Avoid self-references.

  # Remove object from the sequence of base classes. Deriving from both Mapping
  # and object will cause a failure to create a MRO for the updated class
  bases = tuple(b for b in cls.__bases__ if b != object)
  cls = type(cls.__name__, bases + (collections.abc.Mapping,), dct)
  return cls


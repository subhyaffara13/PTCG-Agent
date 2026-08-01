
def lazy_computation():
  """Simple example of lazy computation with `configdict.FieldReference`."""
  ref = config_dict.FieldReference(1)
  print(ref.get())  # Prints 1

  add_ten = ref.get() + 10  # ref.get() is an integer and so is add_ten
  add_ten_lazy = ref + 10  # add_ten_lazy is a FieldReference - NOT an integer

  print(add_ten)  # Prints 11
  print(add_ten_lazy.get())  # Prints 11 because ref's value is 1

  # Addition is lazily computed for FieldReferences so changing ref will change
  # the value that is used to compute add_ten.
  ref.set(5)
  print(add_ten)  # Prints 11
  print(add_ten_lazy.get())  # Prints 15 because ref's value is 5


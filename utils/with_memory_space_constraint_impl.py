
def with_memory_space_constraint_impl(x, *, memory_space):
  del x, memory_space
  raise ValueError("Cannot eagerly run with_memory_space_constraint.")


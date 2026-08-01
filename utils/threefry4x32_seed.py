
def threefry4x32_seed(seed: typing.Array) -> typing.Array:
  """Create a single Threefry 4x32 PRNG key from an integer seed.

  The 4-word key is constructed by splitting the seed into two uint32 values
  and hashing with a fixed counter to fill all 4 words.

  Args:
    seed: A scalar integer array.

  Returns:
    A 4-word uint32 PRNG key with shape (4,).
  """
  return _threefry4x32_seed(seed)


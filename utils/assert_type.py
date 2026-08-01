
def assert_type(typ: type, value: object) -> None:
    __tracebackhide__ = True
    if type(value) != typ:
        raise AssertionError(f"Invalid type {typename(type(value))}, expected {typename(typ)}")


def assert_type(
    inputs: Union[Scalar, Union[Array, Sequence[Array]]],
    expected_types: Union[ArrayDType, Sequence[ArrayDType]]) -> None:
  """Checks that the type of all inputs matches specified ``expected_types``.

  If the expected type is a Python type or abstract dtype (e.g. `np.floating`),
  assert that the input has the same sub-type. If the expected type is a
  concrete dtype (e.g. np.float32), assert that the input's type is the same.

  Example usage:

  .. code-block:: python

    assert_type(7, int)
    assert_type(7.1, float)
    assert_type(False, bool)
    assert_type([7, 8], int)
    assert_type([7, 7.1], [int, float])
    assert_type(np.array(7), int)
    assert_type(np.array(7.1), float)
    assert_type([jnp.array([7, 8]), np.array(7.1)], [int, float])
    assert_type(jnp.array(1., dtype=jnp.bfloat16)), jnp.bfloat16)
    assert_type(jnp.ones(1, dtype=np.int8), np.int8)

  Args:
    inputs: An array or a sequence of arrays or scalars.
    expected_types: A sequence of expected types associated with each input; if
      all inputs have same type, a single type may be passed as
      ``expected_types``.

  Raises:
    AssertionError: If lengths of ``inputs`` and ``expected_types`` don't match;
      if ``expected_types`` contains unsupported pytype;
      if the types of inputs do not match the expected types.
  """
  if not isinstance(inputs, (list, tuple)):
    inputs = [inputs]
  if not isinstance(expected_types, (list, tuple)):
    expected_types = [expected_types] * len(inputs)

  errors = []
  if len(inputs) != len(expected_types):
    raise AssertionError(
        "Length of `inputs` and `expected_types` must match, "
        f"got {len(inputs)} != {len(expected_types)}."
    )
  for idx, (x, expected) in enumerate(zip(inputs, expected_types)):
    dtype = x.dtype if hasattr(x, "dtype") else np.result_type(x)
    if expected in {float, jnp.floating}:
      if not jnp.issubdtype(dtype, jnp.floating):
        errors.append((idx, dtype, expected))
    elif expected in {int, jnp.integer}:
      if not jnp.issubdtype(dtype, jnp.integer):
        errors.append((idx, dtype, expected))
    else:
      expected = np.dtype(expected)
      if dtype != expected:
        errors.append((idx, dtype, expected))

  if errors:
    msg = "; ".join(
        f"input {e[0]} has type {e[1]} but expected {e[2]}" for e in errors)

    raise AssertionError(f"Error in type compatibility check: {msg}.")


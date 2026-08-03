from typing import Any, Callable

def assert_functional_equivalence(
    model_apply_fn: Callable[[Any, Any], Any],
    reference_inputs: Sequence[Any],
    expected_params: Any,
    actual_params: Any,
    tolerance: float = 1e-6,
):
  """Asserts two parameter sets produce equivalent model outputs.

  Runs `model_apply_fn(params, x)` for each reference input against both
  parameter sets and compares the outputs. A NaN or shape mismatch fails
  closed (the comparison is `not max_abs_diff <= tolerance`).

  Args:
    model_apply_fn: `apply(params, x) -> y`.
    reference_inputs: Non-empty sequence of inputs to run through the model.
    expected_params: Reference parameter set.
    actual_params: Parameter set validated against the reference.
    tolerance: Maximum allowed absolute output difference per input.

  Raises:
    ValueError: If `reference_inputs` is empty.
    AssertionError: If any input's output diverges beyond `tolerance`.
  """
  if not reference_inputs:
    raise ValueError("reference_inputs must be a non-empty sequence")
  for idx, x in enumerate(reference_inputs):
    expected_out = np.asarray(
        model_apply_fn(expected_params, x), dtype=np.float64
    )
    actual_out = np.asarray(model_apply_fn(actual_params, x), dtype=np.float64)
    if expected_out.shape != actual_out.shape:
      raise AssertionError(
          f"Output shape mismatch on input {idx}: "
          f"{expected_out.shape} vs {actual_out.shape}"
      )
    diff = (
        float(np.max(np.abs(expected_out - actual_out)))
        if expected_out.size
        else 0.0
    )
    if not diff <= tolerance:
      raise AssertionError(
          f"Functional divergence on input {idx}: "
          f"max_abs_diff={diff} > tolerance={tolerance}"
      )


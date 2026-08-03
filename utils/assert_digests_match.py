from typing import Any

def assert_digests_match(expected_digests: dict[str, str], pytree: Any):
  """Asserts a pytree's per-leaf digests match a previously captured set.

  Args:
    expected_digests: Per-leaf SHA-256 from a prior `digest_pytree` call.
    pytree: The pytree to check.

  Raises:
    AssertionError: If a leaf is missing, unexpected, or its digest differs.
  """
  actual = digest_pytree(pytree)
  for path in sorted(set(expected_digests) ^ set(actual)):
    where = "missing in pytree" if path in expected_digests else "unexpected"
    raise AssertionError(f"Digest key mismatch at {path}: {where}")
  for path, expected in expected_digests.items():
    if actual[path] != expected:
      raise AssertionError(
          f"Digest mismatch at {path}: expected {expected}, got {actual[path]}"
      )


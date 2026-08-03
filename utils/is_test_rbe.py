import os

def is_test_rbe() -> bool:
  """Check for a variable set by the RBE toolchain under testing."""
  return (
      os.getenv("IS_JAX_RBE_TESTING", "").lower() in {"true", "1", "yes", "y"}
      )


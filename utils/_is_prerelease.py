import os

def _is_prerelease() -> bool:
  """Determine if this is a pre-release ("rc" wheels) build."""
  rc_version = os.getenv("WHEEL_VERSION_SUFFIX", "")
  return True if rc_version.startswith("rc") else False


def _is_prerelease() -> bool:
  """Determine if this is a pre-release ("rc" wheels) build."""
  rc_version = os.getenv("WHEEL_VERSION_SUFFIX", "")
  return True if rc_version.startswith("rc") else False


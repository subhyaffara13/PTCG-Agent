
def _safe_check_output(cmd: list[str]) -> str:
  """Runs cmd and returns its stripped stdout, or an empty string on error."""
  try:
    return (
        subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=5)
        .decode("utf-8")
        .strip()
    )
  except (
      subprocess.CalledProcessError,
      FileNotFoundError,
      OSError,
      subprocess.TimeoutExpired,
  ):
    return ""



def try_nvidia_smi() -> str | None:
  try:
    return subprocess.check_output(['nvidia-smi']).decode()
  except Exception:
    return None


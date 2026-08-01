
def get_tpu_version() -> int:
  if device_under_test() != "tpu":
    raise ValueError("Device is not TPU")
  kind = xla_bridge.devices()[0].device_kind
  match = re.match(r"TPU[^\d]*(\d+)", kind)
  if match is None:
    raise ValueError(f"Device kind {kind} is not supported")
  return int(match.group(1))


def get_tpu_version() -> int:
  """Returns the numeric version of the TPU, or -1 if not on TPU."""
  kind = jax.devices()[0].device_kind
  if 'TPU' not in kind:
    return -1
  if kind == 'TPU7x':
    return 7
  if kind.endswith(' lite'):
    kind = kind[: -len(' lite')]
  assert kind[:-1] == 'TPU v', kind
  return int(kind[-1])


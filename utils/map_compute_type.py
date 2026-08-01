
def map_compute_type(c_type: str) -> str:
  if c_type == "device_host":
    return "host"
  elif c_type == "device":
    return "dense"
  elif c_type == "tpu_sparsecore":
    return "sparseoffload"
  raise ValueError(f"Invalid compute type {c_type}. Current supported values "
                   "are `device_host`, `device` and `tpu_sparsecore`")



def get_hardware_type(
    tpu_type: str | None, device_type: str | None
) -> HardwareType:
  """Categorizes a compute instance string into a HardwareType enum."""
  tpu_type = tpu_type.lower().strip() if tpu_type else ''
  device_type = device_type.lower().strip() if device_type else ''
  device_type = tpu_type or device_type

  # 1. Check for TPU
  # Matches GCP TPU names like v2, v3, v4, v5e, v5p, or explicit 'tpu'
  if re.search(r'\bv[2-5][a-z]*\b', device_type) or 'tpu' in device_type:
    return HardwareType.TPU

  # 2. Check for GPU
  # Matches common accelerator names (h100, a100, l4) or GPU (a2, a3, g2, p4)
  gpu_chips = ['h100', 'a100', 'v100', 'p100', 't4', 'l4', 'k80']
  gpu_instances = [r'^a[2-3]-', r'^g[2]-', r'^p[3-5]\.', r'^g[4-5]\.']

  if (
      any(chip in device_type for chip in gpu_chips)
      or any(re.match(pattern, device_type) for pattern in gpu_instances)
      or 'gpu' in device_type
  ):
    return HardwareType.GPU

  # 3. Check for CPU
  # Matches GCP (n1, n2, e2, c2, c3, m1) and AWS (t2, m5, c5)
  cpu_instances = [r'^[necm][1-4]-', r'^[tcmri][2-8]\.']
  if (
      any(re.match(pattern, device_type) for pattern in cpu_instances)
      or 'cpu' in device_type
  ):
    return HardwareType.CPU

  return HardwareType.UNKNOWN


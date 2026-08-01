
def get_num_sms() -> int:
    """Handle experimental carveout if set otherwise return hardware SM count"""
    # TODO we need to properly guard on this global
    if torch.xpu.is_available():
        return get_max_num_sms()
    carveout = torch._C._get_sm_carveout_experimental()
    return get_max_num_sms() - (carveout if carveout is not None else 0)


def get_num_sms() -> int:
  if abstract_device := jax.sharding.get_abstract_mesh().abstract_device:
    return abstract_device.num_cores
  return backend.get_default_device().core_count


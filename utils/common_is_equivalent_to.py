
def common_is_equivalent_to(s1: Sharding, s2: Sharding, ndim: int,
                            check_devices: bool = True) -> bool:
  hlo_s_eq = are_hlo_shardings_equal(
      s1._to_xla_hlo_sharding(ndim), s2._to_xla_hlo_sharding(ndim))
  mem_eq = s1.memory_kind == s2.memory_kind
  if check_devices:
    return (hlo_s_eq and mem_eq and
            s1._internal_device_list == s2._internal_device_list)
  else:
    return hlo_s_eq and mem_eq


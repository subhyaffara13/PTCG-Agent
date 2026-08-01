
def _sharding_indices_and_eq(src_sharding, dst_sharding, ndim):
  hlos_eq = are_hlo_shardings_equal(src_sharding._to_xla_hlo_sharding(ndim),
                                    dst_sharding._to_xla_hlo_sharding(ndim))
  len_eq = (len(src_sharding._internal_device_list.addressable_device_list) ==
            len(dst_sharding._internal_device_list.addressable_device_list))
  return hlos_eq and len_eq



def _tensor_rebuild_functions():
    return {
        torch._utils._rebuild_parameter,
        torch._utils._rebuild_parameter_with_state,
        torch._utils._rebuild_qtensor,
        torch._utils._rebuild_tensor,
        torch._utils._rebuild_tensor_v2,
        torch._utils._rebuild_tensor_v3,
        torch._utils._rebuild_sparse_tensor,
        torch._utils._rebuild_meta_tensor_no_storage,
        torch._utils._rebuild_nested_tensor,
        torch._utils._rebuild_wrapper_subclass,
        # Allowlisting this, but not allowlisting the numpy functions by default
        # Reasoning is that we don't have control over the numpy functions, but
        # this utility is provided by pytorch
        torch._utils._rebuild_device_tensor_from_numpy,
        # In 2.6, we should no longer have a dependency on numpy and the above
        # _rebuild_device_tensor_from_numpy function.
        torch._utils._rebuild_device_tensor_from_cpu_tensor,
    }


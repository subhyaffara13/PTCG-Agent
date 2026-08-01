
def _create_cpu_state_dict(
    state_dict: dict[str, Any], pin_memory: bool = False, share_memory: bool = False
) -> dict[str, Any]:
    """
    Given a state_dict, create another state_dict with the same structure and elements.
    However, all tensors in the returned state_dict are new tensors on CPU. These
    tensors can be placed on pin_memory or share_memory based on the provided arguments.

    .. warning::
        Setting both `pin_memory` and `share_memory` to True significantly increases the
        latency of this method because of the nuances which require us to register memory
        as pinned directly as opposed to relying on the pin_memory cache allocator. This
        option should only be used for long lived tensors which are required to be shared.
        This is not the case as long as at least one of `pin_memory` or `share_memory` is
         set to False.

    """

    def tensor_func(
        obj: torch.Tensor,
        pg: dist.ProcessGroup | None,
        device: torch.device | None,
        _: Any,
    ) -> torch.Tensor:
        if len(obj.size()) == 0:
            return torch.tensor(0, dtype=obj.dtype)

        # sometimes, a tensor might have non-zero size and 0 numel. In this case, pinning memory will fail
        # so we take a best guess at how to replicate the tensor below to maintain symmetry in the returned
        # state dict.
        if obj.numel() == 0 or obj.data_ptr() == 0:
            t = torch.zeros_like(obj, device="cpu")
            if share_memory:
                t = t.share_memory_()
            return t

        if share_memory:
            t = torch.empty(*tuple(obj.size()), dtype=obj.dtype)
            t = t.share_memory_()
            if pin_memory:
                pin_memory_utils.pin_memory(t.data_ptr(), t.numel() * t.element_size())
                weakref.finalize(t, pin_memory_utils.unpin_memory, t.data_ptr())

            return t
        elif pin_memory:
            return torch.empty(*tuple(obj.size()), dtype=obj.dtype).pin_memory()
        else:
            return torch.empty(*tuple(obj.size()), dtype=obj.dtype)

    def dtensor_func(
        obj: DTensor,
        pg: dist.ProcessGroup | None,
        device: torch.device | None,
        _: Any,
    ) -> DTensor:
        if len(obj.size()) == 0:
            return obj

        if obj.device != torch.device("cpu"):
            ret = cast(DTensor, obj.to(device="cpu"))
        else:
            ret = copy.deepcopy(obj)
        ret._local_tensor = tensor_func(ret._local_tensor, pg, device, None)
        return ret

    def sharded_tensor_func(
        obj: ShardedTensor,
        pg: dist.ProcessGroup | None,
        device: torch.device | None,
        _: Any,
    ) -> ShardedTensor:
        if not obj.local_shards():
            return obj

        if obj.device != torch.device("cpu"):
            ret = obj.to(device="cpu")
        else:
            ret = copy.deepcopy(obj)

        for shards in ret.local_shards():
            shards.tensor = tensor_func(shards.tensor, pg, device, None)

        return ret

    ret = _iterate_state_dict(
        state_dict,
        sharded_tensor_func,
        dtensor_func,
        tensor_func,
        pg=None,
        device=None,
        cpu_offload=False,
        ranks_only=(),
        type_check=False,
    )
    return ret


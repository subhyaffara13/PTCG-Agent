
def _register_dtensor_impl() -> None:
    from torch.distributed.tensor import DTensor

    @print.py_impl(DTensor)  # pyrefly: ignore [missing-attribute]
    # pyre-ignore
    def print_dtensor(format_str: str, *args: object, **kwargs: object) -> None:
        # Unwrap DTensors to local tensors via to_local() — no collective is
        # introduced so there is no OOM or performance risk.  Every rank prints
        # its own local view (including Replicate, where to_local() already
        # holds the full tensor).
        #
        # The output is prefixed with [rank N] so users can identify which rank
        # produced each line.
        #
        # If the user needs the global view of a sharded tensor, they can call
        # full_tensor() explicitly before passing it to print.
        import torch.distributed as dist

        local_args = pytree.tree_map_only(DTensor, DTensor.to_local, args)
        local_kwargs = pytree.tree_map_only(DTensor, DTensor.to_local, kwargs)
        if dist.is_initialized() and dist.get_world_size() > 1:
            format_str = f"[rank {dist.get_rank()}] {format_str}"
        print(  # pyrefly: ignore [no-matching-overload]
            format_str, *local_args, **local_kwargs
        )


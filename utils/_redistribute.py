
def _redistribute(
    args: Any,
    all_placements: tuple[Any],
    mesh: Any,
    shape_stride_fn: Callable[[torch.Tensor, Any, Any], tuple[list[int], list[int]]],
) -> GraphArg:
    from torch._dispatch.python import suspend_functionalization
    from torch._guards import detect_fake_mode
    from torch._subclasses.functional_tensor import disable_functional_mode
    from torch.fx.experimental.proxy_tensor import disable_proxy_modes_tracing

    with (
        suspend_functionalization(),
        disable_functional_mode(),
        disable_proxy_modes_tracing(),
    ):
        fake_mode = detect_fake_mode(args)
        if fake_mode is None:
            raise AssertionError("defer_inlining() is only supported for FakeTensors")

        with fake_mode:
            new_args = list(pytree.tree_map(_new_tensor, args))
            for i, (tensor, placements) in enumerate(zip(new_args, all_placements)):
                if tensor is None:
                    # Sometimes gradients can be None
                    continue

                new_shape, new_stride = shape_stride_fn(
                    tensor,
                    mesh,
                    placements,
                )
                new_args[i] = _new_tensor(
                    tensor, new_shape=new_shape, new_stride=new_stride
                )

            new_args = tuple(new_args)
            if not all(
                isinstance(t, (FakeTensor, int, torch.SymInt, type(None)))
                for t in new_args
            ):
                raise AssertionError(f"Unexpected element in {args=}")

    return new_args


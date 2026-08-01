
def aot_eager_decomp_partition_with_mode(
    gm: torch.fx.GraphModule,
    fake_tensor_inputs: list[torch.Tensor],
    mode: Any,
    **kwarg: Any,
) -> Callable[..., Any]:
    return aot_autograd(
        # these are taken from memory_efficient_fusion()
        fw_compiler=functools.partial(boxed_nop_with_mode, mode=mode),
        bw_compiler=functools.partial(boxed_nop_with_mode, mode=mode),
        # NB: lambda here is to delay import of inductor
        decompositions=lambda: import_module(
            "torch._inductor.compile_fx"
        ).select_decomp_table(),
        partition_fn=functools.partial(
            min_cut_rematerialization_partition, compiler="inductor"
        ),
    )(gm, fake_tensor_inputs)


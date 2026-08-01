
def partition_fn(
    gm: GraphModule,
    joint_inputs: Sequence[object],
    **kwargs: object,
) -> tuple[GraphModule, GraphModule]:
    cuda_context = get_cuda_device_context(gm)
    with cuda_context:
        # We can skip the invoke_subgraph because the
        # entire_partition_fn is called recursively for invoke_subgraph
        # in partitioning.
        inputs_devices = get_inputs_devices(joint_inputs, gm)
        gm = _recursive_joint_graph_passes(
            gm,
            skip_invoke_subgraph=True,
            input_device=next(iter(inputs_devices)),
        )

    static_lifetime_input_indices: list[int] | None = kwargs.pop(  # type: ignore[assignment]
        "static_lifetime_input_indices", None
    )

    if config.custom_partitioner_fn is None:
        with dynamo_utils.dynamo_timed(
            "min_cut_rematerialization_partition", log_pt2_compile_event=True
        ):
            return min_cut_rematerialization_partition(
                gm,
                joint_inputs,
                compiler="inductor",
                static_lifetime_input_indices=static_lifetime_input_indices,
                # pyrefly: ignore[bad-argument-type]
                **kwargs,
            )
    else:
        assert isinstance(config.custom_partitioner_fn, CustomPartitionerFn)
        with dynamo_utils.dynamo_timed(
            config.custom_partitioner_fn.__class__.__name__,
            log_pt2_compile_event=True,
        ):
            return config.custom_partitioner_fn(
                gm,
                joint_inputs,
                compiler="inductor",
                static_lifetime_input_indices=static_lifetime_input_indices,
                **kwargs,
            )


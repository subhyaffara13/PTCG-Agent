
def _cache_autograd_info(
    aot_config: AOTConfig,
    flat_args: list[Any],
    compiled_fw_func: Callable[..., Any],
    compiled_bw_func: Callable[..., Any] | None,
    fw_module_str: str | None,
    bw_module_str: str | None,
    joint_graph_str: str | None,
    wrappers: list[CompilerWrapper],
    maybe_subclass_meta: SubclassMeta | None,
    fw_metadata: ViewAndMutationMeta,
    num_fw_outs_saved_for_bw: int,
    _indices_of_inps_to_detach: list[int],
    num_symints_saved_for_bw: int,
    bw_module: torch.fx.GraphModule | None,
) -> tuple[
    GenericAOTAutogradResult[Any, Any] | None,
    Callable[..., Any],
]:
    backward_state_indices = [
        idx for idx, x in enumerate(flat_args) if isinstance(x, BackwardState)
    ]
    if len(backward_state_indices) > 1:
        raise AssertionError(
            f"expected at most 1 backward_state_index, got {len(backward_state_indices)}"
        )

    make_runtime_safe(fw_metadata, maybe_subclass_meta)

    try_save_cache_entry: Callable[..., Any] | None = None
    entry: GenericAOTAutogradResult[Any, Any] | None = None

    if aot_config.cache_info is not None:
        forward_time_taken_ns = time.time_ns() - aot_config.cache_info.start_time_ns

        # NB: aot_config here is technically not needed as an argument: we could just
        # close over aot_config.cache_info, since aot_config never changes.
        # But closing over random variables is confusing IMO, so I'm leaving it.
        def try_save_cache_entry(  # noqa: F811
            compiled_bw_func: Callable[..., Any],
            bw_module: torch.fx.GraphModule,
            _fw_metadata: ViewAndMutationMeta,
            aot_config: AOTConfig,
        ) -> GenericAOTAutogradResult[Any, Any] | None:
            cache_info = aot_config.cache_info

            def should_save_cache() -> bool:
                if should_bundle_autograd_cache():
                    return True
                else:
                    return hasattr(compiled_fw_func, "_fx_graph_cache_key") and hasattr(
                        compiled_bw_func, "_fx_graph_cache_key"
                    )

            if cache_info is not None and should_save_cache():
                if forward_time_taken_ns is None:
                    raise AssertionError("forward_time_taken_ns must not be None")
                # TODO: technically, AOTAutograd does a *little* bit of post processing work
                # in the backward that isn't measured here. But it's small enough that it's not worth
                # the complexity of threading a bunch of times through the code, so we
                # use the compiled_bw_func's inductor compile time instead.
                # It's possible this changes in the future, in which case we should
                # update backward_time_taken_ns to be more inclusive
                backward_time_taken_ns = getattr(compiled_bw_func, "_time_taken_ns", 0)

                aot_forward_graph_str: str | None = fw_module_str
                aot_backward_graph_str: str | None = bw_module_str
                aot_joint_graph_str: str | None = joint_graph_str
                guards_expr = AOTAutogradCache.generate_guards_expression(cache_info)

                entry = AOTAutogradCache.make_entry(
                    compiled_fw_func,  # type: ignore[arg-type]
                    compiled_bw_func,  # type: ignore[arg-type]
                    aot_joint_graph_str,
                    aot_forward_graph_str,
                    aot_backward_graph_str,
                    _fw_metadata,
                    wrappers,
                    maybe_subclass_meta,
                    num_fw_outs_saved_for_bw,
                    _indices_of_inps_to_detach,
                    forward_time_taken_ns,
                    backward_time_taken_ns,
                    sanitized_aot_config=sanitize_aot_config(aot_config),
                    guards_expr=guards_expr,
                    backward_state_indices=backward_state_indices,
                    num_symints_saved_for_bw=num_symints_saved_for_bw,
                    serialized_bw_module=serialize_graph_module(bw_module),
                )
                AOTAutogradCache.save(
                    cache_info.cache_key,
                    entry,
                    remote=should_use_remote_autograd_cache(),
                )
                return entry
            return None

        if compiled_bw_func is not None:
            # If we already compiled the backward, we save its cache entry now
            if bw_module is None:
                raise AssertionError(
                    "bw_module must not be None when compiled_bw_func is not None"
                )
            entry = try_save_cache_entry(
                compiled_bw_func,
                bw_module,
                fw_metadata,
                aot_config,  # type: ignore[arg-type]
            )
            try_save_cache_entry = None

    return try_save_cache_entry, entry  # type: ignore[return-value]


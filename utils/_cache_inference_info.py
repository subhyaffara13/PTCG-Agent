
def _cache_inference_info(
    aot_config: AOTConfig,
    fw_metadata: ViewAndMutationMeta,
    maybe_subclass_meta: SubclassMeta | None,
    compiled_fw: Callable[..., Any],
    aot_forward_graph_str: str | None,
    wrappers: list[CompilerWrapper],
) -> GenericAOTAutogradResult[Any, Any] | None:
    make_runtime_safe(fw_metadata, maybe_subclass_meta)

    cache_info = aot_config.cache_info

    def should_save_cache() -> bool:
        if should_bundle_autograd_cache():
            return True
        else:
            return hasattr(compiled_fw, "_fx_graph_cache_key")

    entry: GenericAOTAutogradResult[Any, Any] | None = None
    if cache_info is not None and should_save_cache():
        time_taken_ns = time.time_ns() - cache_info.start_time_ns
        guards_expr = AOTAutogradCache.generate_guards_expression(cache_info)
        entry = AOTAutogradCache.make_entry(
            compiled_fw_func=compiled_fw,  # type: ignore[arg-type]
            compiled_bw_func=None,
            aot_joint_graph_str=None,
            aot_forward_graph_str=aot_forward_graph_str,
            aot_backward_graph_str=None,
            runtime_metadata=fw_metadata,
            dispatch_wrappers=wrappers,
            maybe_subclass_meta=maybe_subclass_meta,
            num_fw_outs_saved_for_bw=None,
            indices_of_inps_to_detach=[],
            forward_time_taken_ns=time_taken_ns,
            backward_time_taken_ns=0,
            sanitized_aot_config=sanitize_aot_config(aot_config),
            guards_expr=guards_expr,
            backward_state_indices=None,
            num_symints_saved_for_bw=None,
            serialized_bw_module=None,
        )
        AOTAutogradCache.save(
            cache_info.cache_key,
            entry,
            remote=should_use_remote_autograd_cache(),
        )

    return entry



def sanitize_aot_config(input: AOTConfig) -> AOTConfig:
    return AOTConfig(
        fw_compiler=None,
        bw_compiler=None,
        partition_fn=None,
        decompositions={},
        inference_compiler=None,
        num_params_buffers=input.num_params_buffers,
        aot_id=input.aot_id,
        keep_inference_input_mutations=input.keep_inference_input_mutations,
        is_export=input.is_export,
        no_tangents=input.no_tangents,
        aot_autograd_arg_pos_to_source=input.aot_autograd_arg_pos_to_source,
        dynamic_shapes=input.dynamic_shapes,
        enable_log=input.enable_log,
        static_input_indices=input.static_input_indices,
        pre_dispatch=input.pre_dispatch,
        cache_info=None,
        precompile_backend_id=input.precompile_backend_id,
    )


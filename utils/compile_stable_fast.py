
def compile_stable_fast(pipeline, enable_cuda_graph=True):
    from sfast.compilers.stable_diffusion_pipeline_compiler import CompilationConfig, compile  # noqa: PLC0415

    config = CompilationConfig.Default()

    if importlib.util.find_spec("xformers") is not None:
        config.enable_xformers = True

    if importlib.util.find_spec("triton") is not None:
        config.enable_triton = True

    config.enable_cuda_graph = enable_cuda_graph

    pipeline = compile(pipeline, config)
    return pipeline


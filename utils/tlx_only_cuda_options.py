
def tlx_only_cuda_options() -> list[str]:
    if config.is_fbcode():
        try:
            from torch._inductor.fb.tlx_templates.registry import tlx_only_cuda_options

            return tlx_only_cuda_options

        except ImportError:
            return []

    else:
        return []


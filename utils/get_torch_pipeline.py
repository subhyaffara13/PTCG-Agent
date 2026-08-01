
def get_torch_pipeline(model_name: str, disable_safety_checker: bool, enable_torch_compile: bool, use_xformers: bool):
    if "FLUX" in model_name:
        from diffusers import FluxPipeline  # noqa: PLC0415

        pipe = FluxPipeline.from_pretrained(model_name, torch_dtype=torch.bfloat16).to("cuda")
        if enable_torch_compile:
            pipe.transformer.to(memory_format=torch.channels_last)
            pipe.transformer = torch.compile(pipe.transformer, mode="max-autotune", fullgraph=True)
        return pipe

    if "stable-diffusion-3" in model_name:
        from diffusers import StableDiffusion3Pipeline  # noqa: PLC0415

        pipe = StableDiffusion3Pipeline.from_pretrained(model_name, torch_dtype=torch.bfloat16).to("cuda")
        if enable_torch_compile:
            pipe.transformer.to(memory_format=torch.channels_last)
            pipe.transformer = torch.compile(pipe.transformer, mode="max-autotune", fullgraph=True)
        return pipe

    from diffusers import DDIMScheduler, StableDiffusionPipeline  # noqa: PLC0415
    from torch import channels_last, float16  # noqa: PLC0415

    pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=float16).to("cuda")

    pipe.unet.to(memory_format=channels_last)  # in-place operation

    if use_xformers:
        pipe.enable_xformers_memory_efficient_attention()

    if enable_torch_compile:
        pipe.unet = torch.compile(pipe.unet)
        pipe.vae = torch.compile(pipe.vae)
        pipe.text_encoder = torch.compile(pipe.text_encoder)
        print("Torch compiled unet, vae and text_encoder")

    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    pipe.set_progress_bar_config(disable=True)

    if disable_safety_checker:
        pipe.safety_checker = None
        pipe.feature_extractor = None

    return pipe



def load_pipeline(name, engine, use_control_net=False, use_nhwc=False, enable_cuda_graph=True):
    gc.collect()
    torch.cuda.empty_cache()
    before_memory = torch.cuda.memory_allocated()

    scheduler = EulerAncestralDiscreteScheduler.from_pretrained(name, subfolder="scheduler")
    vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16).to("cuda")

    if use_control_net:
        assert "xl" in name
        controlnet = ControlNetModel.from_pretrained("diffusers/controlnet-canny-sdxl-1.0", torch_dtype=torch.float16)
        pipeline = StableDiffusionXLControlNetPipeline.from_pretrained(
            name,
            controlnet=controlnet,
            vae=vae,
            scheduler=scheduler,
            variant="fp16",
            use_safetensors=True,
            torch_dtype=torch.float16,
        ).to("cuda")
    else:
        pipeline = DiffusionPipeline.from_pretrained(
            name,
            vae=vae,
            scheduler=scheduler,
            variant="fp16",
            use_safetensors=True,
            torch_dtype=torch.float16,
        ).to("cuda")
    pipeline.safety_checker = None

    gc.collect()
    after_memory = torch.cuda.memory_allocated()
    print(f"Loaded model with {after_memory - before_memory} bytes allocated")

    if engine == "stable_fast":
        pipeline = compile_stable_fast(pipeline, enable_cuda_graph=enable_cuda_graph)
    elif engine == "torch":
        pipeline = compile_torch(pipeline, use_nhwc=use_nhwc)

    pipeline.set_progress_bar_config(disable=True)
    return pipeline


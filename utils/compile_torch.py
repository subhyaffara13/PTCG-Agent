
def compile_torch(pipeline, use_nhwc=False):
    if use_nhwc:
        pipeline.unet.to(memory_format=torch.channels_last)

    pipeline.unet = torch.compile(pipeline.unet, mode="reduce-overhead", fullgraph=True)

    if hasattr(pipeline, "controlnet"):
        if use_nhwc:
            pipeline.controlnet.to(memory_format=torch.channels_last)
        pipeline.controlnet = torch.compile(pipeline.controlnet, mode="reduce-overhead", fullgraph=True)
    return pipeline


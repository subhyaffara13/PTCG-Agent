
def test_ort_cuda(
    pipeline,
    batch_size=1,
    steps=4,
    control_image=None,
    warmup_runs=3,
    test_runs=10,
    seed=123,
    verbose=False,
    image_height=512,
    image_width=512,
):
    if batch_size > 4 and pipeline.pipeline_info.version == "xl-1.0":
        pipeline.backend.enable_vae_slicing()

    pipeline.load_resources(image_height, image_width, batch_size)

    warmup_prompt = "warm up"
    for _ in range(warmup_runs):
        images, _ = pipeline.run(
            [warmup_prompt] * batch_size,
            [""] * batch_size,
            image_height=image_height,
            image_width=image_width,
            denoising_steps=steps,
            guidance=0.0,
            seed=seed,
            controlnet_images=[control_image],
            controlnet_scales=torch.FloatTensor([0.5]),
            output_type="image",
        )
        assert len(images) == batch_size

    generator = torch.Generator(device="cuda")
    generator.manual_seed(seed)

    prompt = get_prompt()

    latency_list = []
    images = None
    for _ in range(test_runs):
        torch.cuda.synchronize()
        start_time = time.perf_counter()
        images, _ = pipeline.run(
            [prompt] * batch_size,
            [""] * batch_size,
            image_height=image_height,
            image_width=image_width,
            denoising_steps=steps,
            guidance=0.0,
            seed=seed,
            controlnet_images=[control_image],
            controlnet_scales=torch.FloatTensor([0.5]),
            output_type="pil",
        )
        torch.cuda.synchronize()
        seconds = time.perf_counter() - start_time
        latency_list.append(seconds)

    if verbose:
        print(latency_list)

    return images, latency_list


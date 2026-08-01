
def run_pipelines(
    args, base, refiner, prompt, negative_prompt, controlnet_image=None, controlnet_scale=None, is_warm_up=False
):
    image_height = args.height
    image_width = args.width
    batch_size = len(prompt)
    base.load_resources(image_height, image_width, batch_size)
    if refiner:
        refiner.load_resources(image_height, image_width, batch_size)

    def run_base_and_refiner(warmup=False):
        images, base_perf = base.run(
            prompt,
            negative_prompt,
            image_height,
            image_width,
            denoising_steps=args.denoising_steps,
            guidance=args.guidance,
            seed=args.seed,
            controlnet_images=controlnet_image,
            controlnet_scales=controlnet_scale,
            show_latency=not warmup,
            output_type="latent" if refiner else "pil",
        )
        if refiner is None:
            return images, base_perf

        # Use same seed in base and refiner.
        seed = base.get_current_seed()

        images, refiner_perf = refiner.run(
            prompt,
            negative_prompt,
            image_height,
            image_width,
            denoising_steps=args.refiner_denoising_steps,
            image=images,
            strength=args.strength,
            guidance=args.refiner_guidance,
            seed=seed,
            show_latency=not warmup,
        )

        perf_data = None
        if base_perf and refiner_perf:
            perf_data = {"latency": base_perf["latency"] + refiner_perf["latency"]}
            perf_data.update({"base." + key: val for key, val in base_perf.items()})
            perf_data.update({"refiner." + key: val for key, val in refiner_perf.items()})

        return images, perf_data

    if not args.disable_cuda_graph:
        # inference once to get cuda graph
        _, _ = run_base_and_refiner(warmup=True)

    if args.num_warmup_runs > 0:
        print("[I] Warming up ..")
    for _ in range(args.num_warmup_runs):
        _, _ = run_base_and_refiner(warmup=True)

    if is_warm_up:
        return

    print("[I] Running StableDiffusion XL pipeline")
    if args.nvtx_profile:
        cudart.cudaProfilerStart()
    images, perf_data = run_base_and_refiner(warmup=False)
    if args.nvtx_profile:
        cudart.cudaProfilerStop()

    if refiner:
        print("|----------------|--------------|")
        print("| {:^14} | {:>9.2f} ms |".format("e2e", perf_data["latency"]))
        print("|----------------|--------------|")

    metadata = get_metadata(args, True)
    metadata.update({"base." + key: val for key, val in base.metadata().items()})
    if refiner:
        metadata.update({"refiner." + key: val for key, val in refiner.metadata().items()})
    if perf_data:
        metadata.update(perf_data)
    metadata["images"] = len(images)
    print(metadata)
    (refiner or base).save_images(images, prompt, negative_prompt, metadata)


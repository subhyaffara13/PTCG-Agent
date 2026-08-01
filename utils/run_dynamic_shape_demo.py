
def run_dynamic_shape_demo(args):
    """
    Run demo of generating images with different settings with ORT CUDA provider.
    Try "python demo_txt2img_xl.py --max-cuda-graphs 3 --user-compute-stream" to see the effect of multiple CUDA graphs.
    """
    args.engine = "ORT_CUDA"
    base, refiner = load_pipelines(args, 1)

    prompts = [
        "starry night over Golden Gate Bridge by van gogh",
        "beautiful photograph of Mt. Fuji during cherry blossom",
        "little cute gremlin sitting on a bed, cinematic",
        "cute grey cat with blue eyes, wearing a bowtie, acrylic painting",
        "beautiful Renaissance Revival Estate, Hobbit-House, detailed painting, warm colors, 8k, trending on Artstation",
        "blue owl, big green eyes, portrait, intricate metal design, unreal engine, octane render, realistic",
        "An astronaut riding a rainbow unicorn, cinematic, dramatic",
        "close-up photography of old man standing in the rain at night, in a street lit by lamps, leica 35mm",
    ]

    # batch size, height, width, scheduler, steps, prompt, seed, guidance, refiner scheduler, refiner steps, refiner strength
    configs = [
        (1, 832, 1216, "UniPC", 8, prompts[0], None, 5.0, "UniPC", 10, 0.3),
        (1, 1024, 1024, "DDIM", 24, prompts[1], None, 5.0, "DDIM", 30, 0.3),
        (1, 1216, 832, "EulerA", 16, prompts[2], 1716921396712843, 5.0, "EulerA", 10, 0.3),
        (1, 1344, 768, "EulerA", 24, prompts[3], 123698071912362, 5.0, "EulerA", 20, 0.3),
        (2, 640, 1536, "UniPC", 16, prompts[4], 4312973633252712, 5.0, "UniPC", 10, 0.3),
        (2, 1152, 896, "DDIM", 24, prompts[5], 1964684802882906, 5.0, "UniPC", 20, 0.3),
    ]

    # In testing LCM, refiner is disabled so the settings of refiner is not used.
    if args.lcm:
        configs = [
            (1, 1024, 1024, "LCM", 8, prompts[6], None, 1.0, "UniPC", 20, 0.3),
            (1, 1216, 832, "LCM", 6, prompts[7], 1337, 1.0, "UniPC", 20, 0.3),
        ]

    # Warm up each combination of (batch size, height, width) once before serving.
    args.prompt = ["warm up"]
    args.num_warmup_runs = 1
    for batch_size, height, width, _, _, _, _, _, _, _, _ in configs:
        args.batch_size = batch_size
        args.height = height
        args.width = width
        print(f"\nWarm up batch_size={batch_size}, height={height}, width={width}")
        prompt, negative_prompt = repeat_prompt(args)
        run_pipelines(args, base, refiner, prompt, negative_prompt, is_warm_up=True)

    # Run pipeline on a list of prompts.
    args.num_warmup_runs = 0
    for (
        batch_size,
        height,
        width,
        scheduler,
        steps,
        example_prompt,
        seed,
        guidance,
        refiner_scheduler,
        refiner_denoising_steps,
        strength,
    ) in configs:
        args.prompt = [example_prompt]
        args.batch_size = batch_size
        args.height = height
        args.width = width
        args.scheduler = scheduler
        args.denoising_steps = steps
        args.seed = seed
        args.guidance = guidance
        args.refiner_scheduler = refiner_scheduler
        args.refiner_denoising_steps = refiner_denoising_steps
        args.strength = strength
        base.set_scheduler(scheduler)
        if refiner:
            refiner.set_scheduler(refiner_scheduler)
        prompt, negative_prompt = repeat_prompt(args)
        run_pipelines(args, base, refiner, prompt, negative_prompt, is_warm_up=False)

    base.teardown()
    if refiner:
        refiner.teardown()



def set_default_arguments(args):
    # set default value for some arguments if not provided
    if args.height is None:
        args.height = PipelineInfo.default_resolution(args.version)

    if args.width is None:
        args.width = PipelineInfo.default_resolution(args.version)

    is_lcm = (args.version == "xl-1.0" and args.lcm) or "lcm" in args.lora_weights
    is_turbo = args.version in ["sd-turbo", "xl-turbo"]
    if args.denoising_steps is None:
        args.denoising_steps = 4 if is_turbo else 8 if is_lcm else (30 if args.version == "xl-1.0" else 50)

    if args.scheduler is None:
        args.scheduler = "LCM" if (is_lcm or is_turbo) else ("EulerA" if args.version == "xl-1.0" else "DDIM")

    if args.guidance is None:
        args.guidance = 0.0 if (is_lcm or is_turbo) else (5.0 if args.version == "xl-1.0" else 7.5)


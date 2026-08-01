
def load_pipelines(args, batch_size=None):
    engine_type = get_engine_type(args.engine)

    # Register TensorRT plugins
    if engine_type == EngineType.TRT:
        from trt_utilities import init_trt_plugins  # noqa: PLC0415

        init_trt_plugins()

    max_batch_size = max_batch(args)

    if batch_size is None:
        assert isinstance(args.prompt, list)
        batch_size = len(args.prompt) * args.batch_size

    if batch_size > max_batch_size:
        raise ValueError(f"Batch size {batch_size} is larger than allowed {max_batch_size}.")

    # For TensorRT,  performance of engine built with dynamic shape is very sensitive to the range of image size.
    # Here, we reduce the range of image size for TensorRT to trade-off flexibility and performance.
    # This range can cover most frequent shape of landscape (832x1216), portrait (1216x832) or square (1024x1024).
    if args.version == "xl-turbo":
        min_image_size = 512
        max_image_size = 768 if args.engine != "ORT_CUDA" else 1024
    elif args.version == "xl-1.0":
        min_image_size = 832 if args.engine != "ORT_CUDA" else 512
        max_image_size = 1216 if args.engine != "ORT_CUDA" else 2048
    else:
        # This range can cover common used shape of landscape 512x768, portrait 768x512, or square 512x512 and 768x768.
        min_image_size = 512 if args.engine != "ORT_CUDA" else 256
        max_image_size = 768 if args.engine != "ORT_CUDA" else 1024

    params = {
        "version": args.version,
        "is_refiner": False,
        "is_inpaint": False,
        "engine_type": engine_type,
        "work_dir": args.work_dir,
        "engine_dir": args.engine_dir,
        "onnx_opset": args.onnx_opset,
        "scheduler": args.scheduler,
        "height": args.height,
        "width": args.width,
        "nvtx_profile": args.nvtx_profile,
        "use_cuda_graph": not args.disable_cuda_graph,
        "build_dynamic_batch": args.build_dynamic_batch,
        "build_dynamic_shape": args.build_dynamic_shape,
        "min_image_size": min_image_size,
        "max_image_size": max_image_size,
        "max_batch_size": max_batch_size,
        "opt_batch_size": 1 if args.build_dynamic_batch else batch_size,
        "build_all_tactics": args.build_all_tactics,
        "do_classifier_free_guidance": args.guidance > 1.0,
        "controlnet": args.controlnet_type,
        "lora_weights": args.lora_weights,
        "lora_scale": args.lora_scale,
        "use_fp16_vae": "xl" in args.version,
        "use_vae": True,
        "framework_model_dir": args.framework_model_dir,
        "max_cuda_graphs": args.max_cuda_graphs,
    }

    if "xl" in args.version:
        params["lcm"] = args.lcm
        params["use_vae"] = not args.enable_refiner
    base = initialize_pipeline(**params)

    refiner = None
    if "xl" in args.version and args.enable_refiner:
        params["version"] = "xl-1.0"  # Allow SDXL Turbo to use refiner.
        params["is_refiner"] = True
        params["scheduler"] = args.refiner_scheduler
        params["do_classifier_free_guidance"] = args.refiner_guidance > 1.0
        params["lcm"] = False
        params["controlnet"] = None
        params["lora_weights"] = None
        params["use_vae"] = True
        params["use_fp16_vae"] = True
        refiner = initialize_pipeline(**params)

    if engine_type == EngineType.TRT:
        max_device_memory = max(base.backend.max_device_memory(), (refiner or base).backend.max_device_memory())
        _, shared_device_memory = cudart.cudaMalloc(max_device_memory)
        base.backend.activate_engines(shared_device_memory)
        if refiner:
            refiner.backend.activate_engines(shared_device_memory)

    if engine_type == EngineType.ORT_CUDA:
        enable_vae_slicing = args.enable_vae_slicing
        if batch_size > 4 and not enable_vae_slicing and (args.height >= 1024 and args.width >= 1024):
            print(
                "Updating enable_vae_slicing to be True to avoid cuDNN error for batch size > 4 and resolution >= 1024."
            )
            enable_vae_slicing = True
        if enable_vae_slicing:
            (refiner or base).backend.enable_vae_slicing()
    return base, refiner


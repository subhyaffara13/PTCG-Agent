import time

def run_torch(config: TestConfig):
    device_type = config.device.type
    is_cuda = device_type == "cuda"

    # Turn on TF32 for Ampere GPUs which could help when data type is float32.
    if is_cuda and torch.cuda.get_device_properties(0).major >= 8 and config.use_tf32:
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

    enabled_auto_cast = is_cuda and config.dtype != torch.float32
    ort_inputs = config.random_inputs()

    with torch.inference_mode(), torch.autocast(device_type=device_type, dtype=config.dtype, enabled=enabled_auto_cast):
        sam2_model = load_sam2_model(config.sam2_dir, config.model_type, device=config.device)
        if config.component == "image_encoder":
            if is_cuda and config.torch_compile_mode != "none":
                sam2_model.image_encoder.forward = torch.compile(
                    sam2_model.image_encoder.forward,
                    mode=config.torch_compile_mode,  # "reduce-overhead" if you want to reduce latency of first run.
                    fullgraph=True,
                    dynamic=False,
                )

            image_shape = config.shape_dict()["image"]
            img = torch.randn(image_shape).to(device=config.device, dtype=config.dtype)
            sam2_encoder = SAM2ImageEncoder(sam2_model)

            if is_cuda and config.torch_compile_mode != "none":
                print(f"Running warm up. It will take a while since torch compile mode is {config.torch_compile_mode}.")

            for _ in range(config.warm_up):
                _image_features_0, _image_features_1, _image_embeddings = sam2_encoder(img)

            if is_cuda and config.enable_nvtx_profile:
                import nvtx  # noqa: PLC0415
                from cuda import cudart  # noqa: PLC0415

                cudart.cudaProfilerStart()
                print("Start nvtx profiling on encoder ...")
                with nvtx.annotate("one_run"):
                    sam2_encoder(img, enable_nvtx_profile=True)
                cudart.cudaProfilerStop()

            if is_cuda and config.enable_torch_profile:
                with torch.profiler.profile(
                    activities=[torch.profiler.ProfilerActivity.CPU, torch.profiler.ProfilerActivity.CUDA],
                    record_shapes=True,
                ) as prof:
                    print("Start torch profiling on encoder ...")
                    with torch.profiler.record_function("encoder"):
                        sam2_encoder(img)
                print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
                prof.export_chrome_trace("torch_image_encoder.json")

            if config.repeats == 0:
                return

            print(f"Start {config.repeats} runs of performance tests...")
            start = time.time()
            for _ in range(config.repeats):
                _image_features_0, _image_features_1, _image_embeddings = sam2_encoder(img)
                if is_cuda:
                    torch.cuda.synchronize()
        else:
            torch_inputs = (
                ort_inputs["image_features_0"],
                ort_inputs["image_features_1"],
                ort_inputs["image_embeddings"],
                ort_inputs["point_coords"],
                ort_inputs["point_labels"],
                ort_inputs["input_masks"],
                ort_inputs["has_input_masks"],
                ort_inputs["original_image_size"],
            )

            sam2_decoder = SAM2ImageDecoder(
                sam2_model,
                multimask_output=config.multi_mask_output,
            )

            if is_cuda and config.torch_compile_mode != "none":
                sam2_decoder.forward = torch.compile(
                    sam2_decoder.forward,
                    mode=config.torch_compile_mode,
                    fullgraph=True,
                    dynamic=False,
                )

            # warm up
            for _ in range(config.warm_up):
                _masks, _iou_predictions, _low_res_masks = sam2_decoder(*torch_inputs)

            if is_cuda and config.enable_nvtx_profile:
                import nvtx  # noqa: PLC0415
                from cuda import cudart  # noqa: PLC0415

                cudart.cudaProfilerStart()
                print("Start nvtx profiling on decoder...")
                with nvtx.annotate("one_run"):
                    sam2_decoder(*torch_inputs, enable_nvtx_profile=True)
                cudart.cudaProfilerStop()

            if is_cuda and config.enable_torch_profile:
                with torch.profiler.profile(
                    activities=[torch.profiler.ProfilerActivity.CPU, torch.profiler.ProfilerActivity.CUDA],
                    record_shapes=True,
                ) as prof:
                    print("Start torch profiling on decoder ...")
                    with torch.profiler.record_function("decoder"):
                        sam2_decoder(*torch_inputs)
                print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
                prof.export_chrome_trace("torch_image_decoder.json")

            if config.repeats == 0:
                return

            print(f"Start {config.repeats} runs of performance tests...")
            start = time.time()
            for _ in range(config.repeats):
                _masks, _iou_predictions, _low_res_masks = sam2_decoder(*torch_inputs)
                if is_cuda:
                    torch.cuda.synchronize()

        end = time.time()
        return (end - start) / config.repeats


def run_torch(
    model_name: str,
    batch_size: int,
    disable_safety_checker: bool,
    enable_torch_compile: bool,
    use_xformers: bool,
    height: int,
    width: int,
    steps: int,
    num_prompts: int,
    batch_count: int,
    start_memory,
    memory_monitor_type,
    skip_warmup: bool = True,
):
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True

    torch.set_grad_enabled(False)

    load_start = time.time()
    pipe = get_torch_pipeline(model_name, disable_safety_checker, enable_torch_compile, use_xformers)
    load_end = time.time()
    print(f"Model loading took {load_end - load_start} seconds")

    image_filename_prefix = get_image_filename_prefix("torch", model_name, batch_size, steps, disable_safety_checker)

    if not enable_torch_compile:
        with torch.inference_mode():
            result = run_torch_pipeline(
                pipe,
                batch_size,
                image_filename_prefix,
                height,
                width,
                steps,
                num_prompts,
                batch_count,
                start_memory,
                memory_monitor_type,
                skip_warmup=skip_warmup,
            )
    else:
        result = run_torch_pipeline(
            pipe,
            batch_size,
            image_filename_prefix,
            height,
            width,
            steps,
            num_prompts,
            batch_count,
            start_memory,
            memory_monitor_type,
            skip_warmup=skip_warmup,
        )

    result.update(
        {
            "model_name": model_name,
            "directory": None,
            "provider": "compile" if enable_torch_compile else "xformers" if use_xformers else "default",
            "disable_safety_checker": disable_safety_checker,
            "enable_cuda_graph": False,
        }
    )
    return result


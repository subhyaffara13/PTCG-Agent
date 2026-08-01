
def run_pytorch(
    use_gpu,
    model_names,
    model_class,
    config_modifier,
    precision,
    num_threads,
    batch_sizes,
    sequence_lengths,
    repeat_times,
    torchscript,
    torch2,
    cache_dir,
    verbose,
):
    results = []
    if use_gpu and not torch.cuda.is_available():
        logger.error("Please install PyTorch with Cuda, and use a machine with GPU for testing gpu performance.")
        return results

    torch.set_grad_enabled(False)

    for model_name in model_names:
        config = AutoConfig.from_pretrained(model_name, torchscript=torchscript, cache_dir=cache_dir)
        config_modifier.modify(config)
        model = load_pretrained_model(
            model_name,
            config=config,
            cache_dir=cache_dir,
            custom_model_class=model_class,
        )

        if config.model_type in ["vit", "swin"]:
            # These models don't use sequence lengths, so just pick the first sequence length so that the summary still works
            sequence_lengths = [sequence_lengths[0]]
        else:
            tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)

            max_input_size = tokenizer.model_max_length

        logger.debug(f"Model {model}")
        logger.debug(f"Number of parameters {model.num_parameters()}")

        if precision == Precision.FLOAT16:
            model.half()

        device = torch.device("cuda:0" if use_gpu else "cpu")
        model.to(device)

        if precision == Precision.INT8:
            model = QuantizeHelper.quantize_torch_model(model)

        for batch_size in batch_sizes:
            if batch_size <= 0:
                continue

            for sequence_length in sequence_lengths:
                if config.model_type in ["vit", "swin"]:
                    logger.info(
                        f"Run PyTorch on {model_name} with input shape {[batch_size, 3, config.image_size, config.image_size]}"
                    )
                    input_ids = torch.randn(
                        size=(batch_size, 3, config.image_size, config.image_size),
                        dtype=torch.float16 if precision == Precision.FLOAT16 else torch.float32,
                        device=device,
                    )
                else:
                    if max_input_size is not None and sequence_length > max_input_size:
                        continue

                    logger.info(f"Run PyTorch on {model_name} with input shape {[batch_size, sequence_length]}")
                    input_ids = torch.randint(
                        low=0,
                        high=config.vocab_size - 1,
                        size=(batch_size, sequence_length),
                        dtype=torch.long,
                        device=device,
                    )
                try:
                    inference = (
                        torch.jit.trace(model, input_ids) if torchscript else torch.compile(model) if torch2 else model
                    )
                    inference(input_ids)

                    runtimes = timeit.repeat(lambda: inference(input_ids), repeat=repeat_times, number=1)  # noqa: B023

                    result = {
                        "engine": "torchscript" if torchscript else "torch2" if torch2 else "torch",
                        "version": torch.__version__,
                        "providers": "NA",
                        "device": "cuda" if use_gpu else "cpu",
                        "optimizer": "",
                        "precision": precision,
                        "io_binding": "",
                        "model_name": model_name,
                        "inputs": 1,
                        "threads": num_threads,
                        "batch_size": batch_size,
                        "sequence_length": sequence_length,
                        "custom_layer_num": config_modifier.get_layer_num(),
                        "datetime": str(datetime.now()),
                    }
                    result.update(get_latency_result(runtimes, batch_size))
                    logger.info(result)
                    results.append(result)
                except RuntimeError as e:
                    logger.exception(e)
                    torch.cuda.empty_cache()

    return results


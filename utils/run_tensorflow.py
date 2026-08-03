import random

def run_tensorflow(
    use_gpu,
    model_names,
    model_class,
    config_modifier,
    precision,
    num_threads,
    batch_sizes,
    sequence_lengths,
    repeat_times,
    cache_dir,
    verbose,
):
    results = []

    import tensorflow as tf  # noqa: PLC0415

    tf.config.threading.set_intra_op_parallelism_threads(num_threads)

    if not use_gpu:
        tf.config.set_visible_devices([], "GPU")

    if use_gpu and not tf.test.is_built_with_cuda():
        logger.error("Please install Tensorflow-gpu, and use a machine with GPU for testing gpu performance.")
        return results

    if use_gpu:  # Restrict TensorFlow to only use the first GPU
        physical_devices = tf.config.list_physical_devices("GPU")
        try:
            tf.config.set_visible_devices(physical_devices[0], "GPU")
            tf.config.experimental.set_memory_growth(physical_devices[0], True)
            tf.distribute.OneDeviceStrategy(device="/gpu:0")
        except RuntimeError as e:
            logger.exception(e)

    if precision == Precision.FLOAT16 or precision == Precision.INT8:
        raise NotImplementedError("Mixed precision is currently not supported.")

    for model_name in model_names:
        config = AutoConfig.from_pretrained(model_name, cache_dir=cache_dir)
        config_modifier.modify(config)

        model = load_pretrained_model(
            model_name,
            config=config,
            cache_dir=cache_dir,
            custom_model_class=model_class,
            is_tf_model=True,
        )

        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)

        max_input_size = tokenizer.model_max_length

        # Define tf.function-decorated forward functions once per model, outside the
        # batch_size/sequence_length loops. Passing input_ids as an argument (instead
        # of closing over it) allows tf.function to cache traced graphs by input shape
        # rather than retracing on every loop iteration. See issue #14953.
        @run_with_tf_optimizations(do_eager_mode=False, use_xla=False)
        def encoder_forward(input_ids):
            return model(input_ids, training=False)  # noqa: B023

        @run_with_tf_optimizations(do_eager_mode=False, use_xla=False)
        def encoder_decoder_forward(input_ids):
            return model(input_ids, decoder_input_ids=input_ids, training=False)  # noqa: B023

        @run_with_tf_optimizations(do_eager_mode=False, use_xla=False)
        def lxmert_forward(input_ids):
            feats = tf.random.normal([1, 1, config.visual_feat_dim])  # noqa: B023
            pos = tf.random.normal([1, 1, config.visual_pos_dim])  # noqa: B023
            return model(  # noqa: B023
                input_ids,
                visual_feats=feats,
                visual_pos=pos,
                training=False,
            )

        if config.is_encoder_decoder:
            inference = encoder_decoder_forward
        elif isinstance(config, LxmertConfig):
            inference = lxmert_forward
        else:
            inference = encoder_forward

        for batch_size in batch_sizes:
            if batch_size <= 0:
                continue

            for sequence_length in sequence_lengths:
                if max_input_size is not None and sequence_length > max_input_size:
                    continue

                logger.info(f"Run Tensorflow on {model_name} with input shape {[batch_size, sequence_length]}")

                rng = random.Random()
                values = [rng.randint(0, config.vocab_size - 1) for i in range(batch_size * sequence_length)]
                input_ids = tf.constant(values, shape=(batch_size, sequence_length), dtype=tf.int32)

                try:
                    inference(input_ids)

                    runtimes = timeit.repeat(lambda: inference(input_ids), repeat=repeat_times, number=1)  # noqa: B023

                    result = {
                        "engine": "tensorflow",
                        "version": tf.__version__,
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
                    from numba import cuda  # noqa: PLC0415

                    device = cuda.get_current_device()
                    device.reset()

    return results


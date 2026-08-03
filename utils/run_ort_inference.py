import os

def run_ort_inference(args, init_inputs, iter_inputs, model):
    def prepare_ort_inputs(inputs, kv_cache_ortvalues):
        # Verify model inputs
        inputs = verify_ort_inputs(model, inputs)

        # Add IO bindings for non-CPU execution providers
        if args.device != "cpu":
            io_binding, kv_cache_ortvalues = add_io_bindings_as_ortvalues(
                model, inputs, args.device, int(args.rank), args.use_buffer_share, kv_cache_ortvalues
            )
            setattr(args, "io_binding", io_binding)  # noqa: B010
            return io_binding, kv_cache_ortvalues

        return inputs, kv_cache_ortvalues

    def with_io_binding(io_binding):
        # Inference pass with IO binding
        model.run_with_iobinding(io_binding)

    def without_io_binding(inputs):
        # Inference pass without IO binding
        outputs = model.run(None, inputs)
        return outputs

    generate_fn = with_io_binding if args.device != "cpu" else without_io_binding
    kv_cache_ortvalues = {}

    if args.profile:
        ort_init_inputs, kv_cache_ortvalues = prepare_ort_inputs(init_inputs, kv_cache_ortvalues)
        new_logname = profile_fn(args, generate_fn, ort_init_inputs, "prompt")

        # Turn profiling off to stop appending to log file
        old_logname = model.end_profiling()
        logger.warning(f"Renaming {old_logname} to {new_logname}")
        os.rename(old_logname, os.path.join(args.log_folder, new_logname))

        # Re-initialize model for new log file instead of appending to old log file
        model = get_model(args)
        ort_iter_inputs, kv_cache_ortvalues = prepare_ort_inputs(iter_inputs, kv_cache_ortvalues)
        new_logname = profile_fn(args, generate_fn, ort_iter_inputs, "token")

        # Turn profiling off to stop appending to log
        old_logname = model.end_profiling()
        logger.warning(f"Renaming {old_logname} to {new_logname}")
        os.rename(old_logname, os.path.join(args.log_folder, new_logname))
        return

    # ORT evaluations
    logger.info("\nEvaluating `model(inputs)` step to get past_key_values")
    ort_init_inputs, kv_cache_ortvalues = prepare_ort_inputs(init_inputs, kv_cache_ortvalues)
    time_fn(args, generate_fn, ort_init_inputs)
    measure_fn(args, generate_fn, ort_init_inputs)

    logger.info("\nEvaluating `model(inputs)` step with past_key_values")
    ort_iter_inputs, kv_cache_ortvalues = prepare_ort_inputs(iter_inputs, kv_cache_ortvalues)
    time_fn(args, generate_fn, ort_iter_inputs)
    measure_fn(args, generate_fn, ort_iter_inputs)


def run_ort_inference(args, inputs, model):
    def prepare_ort_inputs(inputs, warmup=False):
        # Check that all model inputs will be provided
        model_inputs = {model_input.name for model_input in model.get_inputs()}
        user_inputs = set(inputs.keys())
        missing_inputs = model_inputs - user_inputs
        if len(missing_inputs):
            logger.error(f"The following model inputs are missing: {missing_inputs}")
            raise Exception("There are missing inputs to the model. Please add them and try again.")

        # Remove unnecessary inputs from model inputs
        unnecessary_inputs = user_inputs - model_inputs
        if len(unnecessary_inputs):
            for unnecessary_input in unnecessary_inputs:
                logger.info(f"Removing unnecessary input '{unnecessary_input}' from user provided inputs")
                del inputs[unnecessary_input]

        # Add IO bindings for non-CPU execution providers
        if args.device != "cpu":
            io_binding = model.io_binding()
            for k, v in inputs.items():
                io_binding.bind_cpu_input(k, v)
            for output in model.get_outputs():
                io_binding.bind_output(output.name, device_type=args.device, device_id=args.device_id)
            return io_binding

        return inputs

    def with_io_binding(io_binding):
        # Inference pass with IO binding
        model.run_with_iobinding(io_binding)
        return io_binding

    def without_io_binding(inputs):
        # Inference pass without IO binding
        outputs = model.run(None, inputs)
        return outputs

    def handle_output(output):
        if args.eos_token_id in output:
            first_end = np.where(output == args.eos_token_id)[0][0]
            return output[: first_end + 1]

        return output

    generate_fn = with_io_binding if args.device != "cpu" else without_io_binding
    ort_inputs = prepare_ort_inputs(inputs)

    if args.profile:
        new_logname = profile_fn(args, generate_fn, ort_inputs, "e2e")

        # Turn profiling off to stop appending to log file
        old_logname = model.end_profiling()
        logger.warning(f"Renaming {old_logname} to {new_logname}")
        os.rename(old_logname, os.path.join(args.log_folder, new_logname))

        return

    # ORT evaluation
    logger.info("\nEvaluating ONNX Runtime...")
    ort_evaluate_inputs = ort_inputs

    time_fn(args, generate_fn, ort_evaluate_inputs)
    ort_outputs = generate_fn(ort_inputs)
    if args.device != "cpu":
        ort_outputs = ort_outputs.copy_outputs_to_cpu()
    ort_outputs = ort_outputs[0]

    if args.has_audio_stream:
        # ONNX E2E model from Olive produces transcribed output
        logger.info(f"Transcription: {ort_outputs[0][0]}")
    else:
        # convert_to_onnx model produces generated ids
        actual_output = handle_output(ort_outputs[0][0])
        logger.info(f"Generated token length: {len(actual_output)} tokens")
        transcription = args.processor.batch_decode(ort_outputs[0], skip_special_tokens=True)[0]
        # print to stdout as the output for comparison
        print(f"{transcription}")

    measure_fn(args, generate_fn, ort_inputs)


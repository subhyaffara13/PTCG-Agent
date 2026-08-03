import os

def run_hf_inference(args, init_inputs, iter_inputs, model):
    # Inference steps to measure
    def get_logits(inputs):
        # Inference pass without decoding
        outputs = model(**inputs)
        return outputs

    # Examples of other inference steps that can be measured:
    # To use, uncomment the function and assign it to `generate_fn`

    # def get_pred_ids(inputs):
    #     # Inference pass with predicted token ids generation
    #     predicted_ids = model.generate(**inputs)
    #     return predicted_ids

    # def gen_and_dec(inputs):
    #     # Inference pass with generation and decoding
    #     predicted_ids = get_pred_ids(inputs)
    #     transcription = []
    #     for bs in range(args.batch_size):
    #         for rs in range(args.num_return_sequences):
    #             transcription.append(
    #                 args.tokenizer.batch_decode(
    #                     predicted_ids[bs * args.num_return_sequences + rs], skip_special_tokens=True
    #                 )[0]
    #             )
    #     return transcription

    generate_fn = get_logits

    if args.benchmark_type == "hf-pt-compile":
        # Run forward pass once with each set of inputs to process through Dynamo
        generate_fn(init_inputs)
        generate_fn(iter_inputs)

    if args.profile:
        new_logname = profile_fn(args, generate_fn, init_inputs, "prompt")
        if args.benchmark_type == "hf-ort":
            # Turn profiling off to stop appending to log
            old_logname = model.decoder.session.end_profiling()
            logger.warning(f"Renaming {old_logname} to {new_logname}")
            os.rename(old_logname, os.path.join(args.log_folder, new_logname))

        new_logname = profile_fn(args, generate_fn, iter_inputs, "token")
        if args.benchmark_type == "hf-ort":
            # Turn profiling off to stop appending to log
            old_logname = model.decoder_with_past.session.end_profiling()
            logger.warning(f"Renaming {old_logname} to {new_logname}")
            os.rename(old_logname, os.path.join(args.log_folder, new_logname))

        return

    # PyTorch evaluations
    logger.info("\nEvaluating `model(inputs)` step to get past_key_values")
    time_fn(args, generate_fn, init_inputs)
    measure_fn(args, generate_fn, init_inputs)

    logger.info("\nEvaluating `model(inputs)` step with past_key_values")
    time_fn(args, generate_fn, iter_inputs)
    measure_fn(args, generate_fn, iter_inputs)


def run_hf_inference(args, inputs, model):
    # Inference steps to measure
    def get_pred_ids(inputs):
        # Inference pass with predicted token ids generation
        predicted_ids = model.generate(**inputs)
        return predicted_ids

    def gen_and_dec(inputs):
        # Inference pass with generation and decoding
        predicted_ids = get_pred_ids(inputs)
        transcription = []
        for _ in range(args.num_return_sequences):
            transcription.append(args.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0])
        return predicted_ids, transcription

    # Examples of other inference steps that can be measured:
    # To use, uncomment the function and assign it to `generate_fn`

    # def get_logits(inputs):
    #     # Inference pass without decoding
    #     outputs = model(**inputs)
    #     return outputs

    generate_fn = gen_and_dec

    if args.benchmark_type == "hf-pt-compile":
        # Run forward pass once with each set of inputs to process through Dynamo
        generate_fn(inputs)

    if args.profile:
        new_logname = profile_fn(args, generate_fn, inputs, "gen-and-dec")
        if args.benchmark_type == "hf-ort":
            # Rename log files per model component and turn profiling off to stop appending to log
            new_prefix = new_logname[: -len(".json")]

            old_logname = model.encoder.session.end_profiling()
            new_logname = new_prefix + "-encoder.json"
            if os.path.isfile(old_logname):
                logger.warning(f"Renaming {old_logname} to {new_logname}")
                os.rename(old_logname, os.path.join(args.log_folder, new_logname))

            old_logname = model.decoder.session.end_profiling()
            new_logname = new_prefix + "-decoder.json"
            if os.path.isfile(old_logname):
                logger.warning(f"Renaming {old_logname} to {new_logname}")
                os.rename(old_logname, os.path.join(args.log_folder, new_logname))

            old_logname = model.decoder_with_past.session.end_profiling()
            new_logname = new_prefix + "-decoder-with-past.json"
            if os.path.isfile(old_logname):
                logger.warning(f"Renaming {old_logname} to {new_logname}")
                os.rename(old_logname, os.path.join(args.log_folder, new_logname))

        return

    # PyTorch evaluations
    logger.info("\nEvaluating PyTorch...")
    time_fn(args, generate_fn, inputs)
    predicted_ids, transcription = generate_fn(inputs)
    logger.info(f"Generated token length: {len(predicted_ids[0])} tokens")
    logger.info(f"Transcription: {transcription[0]}")
    measure_fn(args, generate_fn, inputs)


import random

def get_inputs(input_data_path: str) -> list[torch.Tensor]:
    """
    Return a random input for the given inputs meta generated from _save_fx_default.
    """
    inputs: list[torch.Tensor] = []
    with open(input_data_path, "rb") as f:
        inputs_meta = pickle.load(f)
        inputs = []
        for meta in inputs_meta:
            if len(meta) == 1:
                type = meta
                input_ = type(random.random())
            else:
                type, shape, _stride, dtype, device = meta
                if dtype in {
                    torch.int,
                    torch.int32,
                    torch.int64,
                    torch.bool,
                    torch.int,
                    torch.uint8,
                    int,
                    float,
                }:
                    input_ = torch.randint(0, 1, shape, dtype=dtype, device=device)
                else:
                    input_ = torch.rand(shape, dtype=dtype, device=device)
            inputs.append(input_)
    return inputs


def get_inputs(args: argparse.Namespace, ort_model_inputs_len: int):
    init_inputs, iter_inputs = None, None

    # For past_present_share_buffer:
    # Set max_seq_len to 2048 for Microsoft LLaMA-2 model since that is the max value currently supported
    # Set max_seq_len to config value for other models
    max_seq_len = 2048 if args.benchmark_type == "ort-msft" else args.config.max_position_embeddings

    if args.benchmark_type in {"hf-pt-eager", "hf-pt-compile"}:
        init_inputs = get_sample_inputs(
            args.config,
            args.target_device,
            args.batch_size,
            args.sequence_length,
            return_dict=True,
        )
        iter_inputs = get_sample_with_past_kv_inputs(
            args.config,
            args.target_device,
            args.batch_size,
            args.sequence_length,
            use_fp16=args.use_fp16,
            return_dict=True,
        )

    elif args.benchmark_type in {"hf-ort"}:
        if ort_model_inputs_len == 3:  # [input_ids, attention_mask, position_ids]
            # Using split models in Optimum (e.g. created by Optimum export)
            init_inputs = get_sample_inputs(
                args.config,
                args.target_device,
                args.batch_size,
                args.sequence_length,
                return_dict=True,
            )
            iter_inputs = get_sample_with_past_kv_inputs(
                args.config,
                args.target_device,
                args.batch_size,
                args.sequence_length,
                use_fp16=args.use_fp16,
                return_dict=True,
            )
        else:
            # Using merged model in Optimum (e.g. created by convert_to_onnx export)
            init_inputs = get_merged_sample_with_past_kv_inputs(
                args.config,
                args.target_device,
                args.batch_size,
                seq_len=args.sequence_length,
                past_seq_len=0,
                max_seq_len=max_seq_len,
                use_fp16=args.use_fp16,
                use_buffer_share=args.use_buffer_share,
                engine="pt",
                return_dict=True,
            )
            iter_inputs = get_merged_sample_with_past_kv_inputs(
                args.config,
                args.target_device,
                args.batch_size,
                seq_len=1,
                past_seq_len=args.sequence_length,
                max_seq_len=max_seq_len,
                use_fp16=args.use_fp16,
                use_buffer_share=args.use_buffer_share,
                engine="pt",
                return_dict=True,
            )

    elif args.benchmark_type == "ort-convert-to-onnx":
        # Microsoft export from convert_to_onnx
        init_inputs = get_merged_sample_with_past_kv_inputs(
            args.config,
            args.target_device,
            args.batch_size,
            seq_len=args.sequence_length,
            past_seq_len=0,
            max_seq_len=max_seq_len,
            use_fp16=args.use_fp16,
            use_buffer_share=args.use_buffer_share,
            engine="ort",
            return_dict=True,
            world_size=args.world_size,
        )
        iter_inputs = get_merged_sample_with_past_kv_inputs(
            args.config,
            args.target_device,
            args.batch_size,
            seq_len=1,
            past_seq_len=args.sequence_length,
            max_seq_len=max_seq_len,
            use_fp16=args.use_fp16,
            use_buffer_share=args.use_buffer_share,
            engine="ort",
            return_dict=True,
            world_size=args.world_size,
        )

    elif args.benchmark_type == "ort-msft":
        # Microsoft export from https://github.com/microsoft/Llama-2-Onnx
        split_kv = ort_model_inputs_len > 5  # original inputs: [x, attn_mask, k_cache, v_cache, pos]

        init_inputs = get_msft_sample_inputs(
            args.config,
            args.batch_size,
            past_seq_len=0,
            seq_len=args.sequence_length,
            max_seq_len=max_seq_len,
            use_fp16=args.use_fp16,
            use_buffer_share=args.use_buffer_share,
            split_kv=split_kv,
        )
        iter_inputs = get_msft_sample_inputs(
            args.config,
            args.batch_size,
            past_seq_len=args.sequence_length,
            seq_len=1,
            max_seq_len=max_seq_len,
            use_fp16=args.use_fp16,
            use_buffer_share=args.use_buffer_share,
            split_kv=split_kv,
        )

    else:
        raise Exception("Unable to auto-detect inputs for provided model")

    return init_inputs, iter_inputs


def get_inputs(args: argparse.Namespace, config: AutoConfig):
    # Dummy values for parity
    world_size = get_size()
    batch_size = 2
    past_sequence_length, sequence_length, max_sequence_length = get_sequence_lengths(args, config)

    if args.merged:
        inputs = get_merged_sample_with_past_kv_inputs(
            config,
            args.device,
            batch_size,
            seq_len=sequence_length,
            past_seq_len=past_sequence_length,
            max_seq_len=max_sequence_length,
            use_fp16=args.use_fp16,
            use_buffer_share=args.use_buffer_share,
            return_dict=True,
            world_size=world_size,
        )
    elif args.use_past_kv:
        inputs = get_sample_with_past_kv_inputs(
            config,
            args.device,
            batch_size,
            sequence_length,
            use_fp16=args.use_fp16,
            return_dict=True,
            world_size=world_size,
        )
    else:
        inputs = get_sample_inputs(config, args.device, batch_size, sequence_length, return_dict=True)

    return inputs


def get_inputs(args: argparse.Namespace):
    if args.benchmark_type not in {"hf-pt-eager", "hf-pt-compile", "hf-ort", "ort"}:
        raise Exception("Unable to auto-detect inputs for provided model")

    def load_via_ffmpeg():
        audio = whisper.load_audio(args.audio_path)
        audio = whisper.pad_or_trim(audio)
        return audio

    def load_via_numpy():
        with open(args.audio_path, "rb") as f:
            audio = np.asarray(list(f.read()), dtype=np.uint8)
            audio = np.array([audio])
        return audio

    inputs = {
        "max_length": args.max_length,
        "min_length": args.min_length,
        "num_beams": args.num_beams,
        "num_return_sequences": args.num_return_sequences,
        "length_penalty": args.length_penalty,
        "repetition_penalty": args.repetition_penalty,
    }
    if args.benchmark_type == "ort":
        # convert_to_onnx export or ONNX E2E solution created by Olive
        for k, v in inputs.items():
            inputs[k] = np.array([v], dtype=np.float32 if "penalty" in k else np.int32)
        if args.has_decoder_input_ids:
            inputs["decoder_input_ids"] = np.array([args.decoder_input_ids], dtype=np.int32)
        if args.has_logits_processor:
            inputs["logits_processor"] = np.array([args.logits_processor], dtype=np.int32)
        if args.has_temperature:
            inputs["temperature"] = np.array([args.temperature], dtype=np.float32)

    # Measure time taken to load audio file
    logger.info(f"Load audio: {args.audio_path}")
    load_audio_fn = lambda onnx_e2e: load_via_numpy() if onnx_e2e else load_via_ffmpeg()  # noqa: E731
    time_fn(args, load_audio_fn, args.has_audio_stream)
    audio_data = load_audio_fn(args.has_audio_stream)

    if args.has_audio_stream:
        # ONNX E2E solution created by Olive
        inputs["audio_stream"] = audio_data
        return inputs

    # Measure time taken to get input features
    logger.info("Feature extraction: ")
    return_type = "np" if args.benchmark_type == "ort" else "pt"
    processor_fn = lambda audio: args.processor.feature_extractor(  # noqa: E731
        [audio], return_tensors=return_type, sampling_rate=args.sampling_rate
    ).input_features
    time_fn(args, processor_fn, audio_data)
    input_features = processor_fn(audio_data)

    if args.benchmark_type == "ort":
        # convert_to_onnx export
        inputs["input_features"] = input_features
        return inputs

    inputs["inputs"] = input_features.to(
        dtype=torch.float16 if args.use_fp16 else torch.float32, device=args.target_device
    )
    inputs["no_repeat_ngram_size"] = args.no_repeat_ngram_size
    inputs["early_stopping"] = True
    inputs["use_cache"] = True

    if args.decoder_input_ids:
        inputs["forced_decoder_ids"] = args.decoder_input_ids

    return inputs


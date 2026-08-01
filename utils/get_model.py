
def get_model(obj: Union[Type['BaseModel'], Type['Dataclass']]) -> Type['BaseModel']:
    from pydantic.v1.main import BaseModel

    try:
        model_cls = obj.__pydantic_model__  # type: ignore
    except AttributeError:
        model_cls = obj

    if not issubclass(model_cls, BaseModel):
        raise TypeError('Unsupported type, must be either BaseModel or dataclass')
    return model_cls


def get_model(args: argparse.Namespace):
    model, sess_options = None, None
    start_time, end_time = None, None

    # There are multiple sources that the model could come from:
    # 1) Benchmark LLaMA-2 from unofficial source on Hugging Face
    # 2) Benchmark LLaMA-2 from official source on Hugging Face, which requires an authentication token
    # 3) Benchmark LLaMA-2 from local download of model
    # 4) Benchmark LLaMA-2 from Microsoft (already optimized, available at https://github.com/microsoft/Llama-2-Onnx)
    # 5) Benchmark LLaMA-2 from convert_to_onnx

    if args.benchmark_type in {"hf-pt-eager", "hf-pt-compile"}:
        source = args.hf_pt_dir_path if args.hf_pt_dir_path else args.model_name
        start_time = time.time()
        model = AutoModelForCausalLM.from_pretrained(
            source,
            torch_dtype=torch.float16 if args.use_fp16 else torch.float32,
            use_auth_token=args.auth,
            trust_remote_code=args.auth,
            use_cache=True,
            cache_dir=args.cache_dir,
        ).to(args.target_device)
        end_time = time.time()

        if args.benchmark_type == "hf-pt-compile":
            model = torch.compile(model)

    elif args.benchmark_type in {"hf-ort", "ort-msft", "ort-convert-to-onnx"}:
        sess_options = ort.SessionOptions()
        sess_options.enable_profiling = args.profile
        if args.verbose:
            sess_options.log_verbosity_level = 1
            sess_options.log_severity_level = 1

    else:
        raise Exception(f"Cannot recognize {args.benchmark_type}")

    if args.benchmark_type == "hf-ort":
        # Optimum export or convert_to_onnx.py export
        provider = args.execution_provider[0] if type(args.execution_provider) is tuple else args.execution_provider
        provider_options = args.execution_provider[1] if type(args.execution_provider) is tuple else None

        decoder_file_name = None
        decoder_with_past_file_name = None
        for filename in os.listdir(args.hf_ort_dir_path):
            if ".onnx" not in filename or ".onnx_data" in filename or ".onnx.data" in filename:
                continue
            if "decoder_model" in filename or filename == "model.onnx":
                decoder_file_name = filename
            if "decoder_with_past_model" in filename:
                decoder_with_past_file_name = filename
            if "decoder_merged_model" in filename:
                decoder_file_name = filename
                decoder_with_past_file_name = filename

        start_time = time.time()
        model = ORTModelForCausalLM.from_pretrained(
            args.hf_ort_dir_path,
            decoder_file_name=decoder_file_name,
            decoder_with_past_file_name=decoder_with_past_file_name,
            use_auth_token=args.auth,
            trust_remote_code=args.auth,
            use_io_binding=True,  # Large perf gain even for cpu due to avoiding output copy.
            use_merged=(True if decoder_file_name == "model.onnx" else None),
            provider=provider,
            provider_options=provider_options,
            session_options=sess_options,
        )
        end_time = time.time()

    if args.benchmark_type in {"ort-msft", "ort-convert-to-onnx"}:
        # Ex: Microsoft export from https://github.com/microsoft/Llama-2-Onnx
        logger.info(f"Loading model from {args.ort_model_path.format(args.rank)}")
        start_time = time.time()
        model = ort.InferenceSession(
            args.ort_model_path.format(args.rank),
            sess_options,
            providers=[args.execution_provider],
        )
        end_time = time.time()

    logger.info(f"Loaded model in {end_time - start_time} s")
    return model


def get_model(args: argparse.Namespace):
    if args.benchmark_type in {"pt-eager", "pt-compile"}:
        model = None
        if args.onnx_precision == "int4" and args.device == "cuda":
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )

            model = AutoModelForCausalLM.from_pretrained(
                args.hf_dir_path if args.hf_dir_path != "" else args.model_name,
                cache_dir=args.cache_dir,
                torch_dtype=args.torch_dtype,
                use_auth_token=args.auth,
                trust_remote_code=args.trust,
                use_cache=True,
                attn_implementation="flash_attention_2",
                quantization_config=bnb_config,
                max_memory={args.device_id: "80GB"},
            )
        else:
            try:
                model = AutoModelForCausalLM.from_pretrained(
                    args.hf_dir_path if args.hf_dir_path != "" else args.model_name,
                    cache_dir=args.cache_dir,
                    torch_dtype=args.torch_dtype,
                    use_auth_token=args.auth,
                    trust_remote_code=args.trust,
                    use_cache=True,
                    attn_implementation=("flash_attention_2" if args.device == "cuda" else "sdpa"),
                ).to(args.target_device)
            except Exception as e:
                # When flash_attention or sdpa doesn't support a model, it throws an exception.
                # Rather than stopping a process, run as eager mode.
                print("Try to load a model using eager mode: ", e)
                model = AutoModelForCausalLM.from_pretrained(
                    args.hf_dir_path if args.hf_dir_path != "" else args.model_name,
                    cache_dir=args.cache_dir,
                    torch_dtype=args.torch_dtype,
                    use_auth_token=args.auth,
                    trust_remote_code=args.trust,
                    use_cache=True,
                    attn_implementation="eager",
                ).to(args.target_device)

        model.eval()

        if args.benchmark_type == "pt-compile":
            model = torch.compile(model)

    else:
        sess_options = ort.SessionOptions()
        ep = (
            ("CUDAExecutionProvider", {"device_id": args.device_id})
            if args.device == "cuda"
            else "CPUExecutionProvider"
        )
        model = ort.InferenceSession(args.onnx_model_path, sess_options=sess_options, providers=[ep])

    return model


def get_model(args: argparse.Namespace):
    model, sess_options = None, None
    start_time, end_time = None, None

    # There are multiple sources that the model could come from:
    # 1) Benchmark Whisper from Hugging Face
    # 2) Benchmark Whisper ONNX model from Optimum export (without pre/post processing)
    # 3) Benchmark Whisper ONNX E2E model from Olive (with pre/post processing)

    if args.benchmark_type in {"hf-pt-eager", "hf-pt-compile"}:
        source = args.hf_pt_model_path if args.hf_pt_model_path else args.model_name
        start_time = time.time()
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            source,
            torch_dtype=torch.float16 if args.use_fp16 else torch.float32,
            use_cache=True,
        ).to(args.target_device)
        end_time = time.time()

        if args.benchmark_type == "hf-pt-compile":
            model = torch.compile(model)

    elif args.benchmark_type in {"hf-ort", "ort"}:
        sess_options = ort.SessionOptions()
        sess_options.enable_profiling = args.profile
        sess_options.register_custom_ops_library(get_library_path())
        if args.verbose:
            sess_options.log_verbosity_level = 1
            sess_options.log_severity_level = 1

    else:
        raise Exception(f"Cannot recognize {args.benchmark_type}")

    if args.benchmark_type == "hf-ort":
        # Optimum export
        provider = args.execution_provider[0] if type(args.execution_provider) is tuple else args.execution_provider
        provider_options = args.execution_provider[1] if type(args.execution_provider) is tuple else None

        start_time = time.time()
        model = ORTModelForSpeechSeq2Seq.from_pretrained(
            args.hf_ort_dir_path,
            provider=provider,
            provider_options=provider_options,
            session_options=sess_options,
            use_io_binding=True,  # Avoid memory copy overhead
        )
        end_time = time.time()

    if args.benchmark_type == "ort":
        # convert_to_onnx.py export
        logger.info(f"Loading model from {args.ort_model_path}")
        start_time = time.time()
        model = ort.InferenceSession(
            args.ort_model_path,
            sess_options,
            providers=[args.execution_provider],
        )
        end_time = time.time()

    logger.info(f"Loaded model in {end_time - start_time} s")

    return model


def get_model(
    ctx: click.Context, model_id: Optional[str], model_name: Optional[str]
) -> None:
    """Get information about a specific model"""
    if not model_id and not model_name:
        raise click.UsageError("Either --id or --name must be provided")

    client = create_client(ctx)
    result = client.models.get(model_id=model_id, model_name=model_name)
    rich.print_json(data=result)


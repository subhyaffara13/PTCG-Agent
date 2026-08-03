import os
from typing import Any, Tuple, Union

def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("url", help="The URL to try and cache")
    return parser.parse_args()


def get_args(argspec, n):
    if isinstance(argspec, np.ndarray):
        args = argspec.copy()
    else:
        nargs = len(argspec)
        ms = np.asarray(
            [1.5 if isinstance(spec, ComplexArg) else 1.0 for spec in argspec]
        )
        ms = (n**(ms/sum(ms))).astype(int) + 1

        args = [spec.values(m) for spec, m in zip(argspec, ms)]
        args = np.array(np.broadcast_arrays(*np.ix_(*args))).reshape(nargs, -1).T

    return args


def get_args(v: Any) -> Any:
    pydantic_generic_metadata: PydanticGenericMetadata | None = getattr(v, '__pydantic_generic_metadata__', None)
    if pydantic_generic_metadata:
        return pydantic_generic_metadata.get('args')
    return typing_extensions.get_args(v)


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("url", help="The URL to try and cache")
    return parser.parse_args()


def get_args(tp: type[Any]) -> tuple[Any, ...]:
    return _get_args(tp)


def get_args() -> argparse:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npz_file_path", type=str, required=True)
    parser.add_argument("--output_file_path", type=str, required=True)
    parser.add_argument("--adapter_version", type=int, required=True)
    parser.add_argument("--model_version", type=int, required=True)
    return parser.parse_args()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input model")
    parser.add_argument("--output", required=True, help="output model")
    args = parser.parse_args()
    return args


def get_args(rank=0):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-bt",
        "--benchmark-type",
        type=str,
        required=True,
        choices=[
            "hf-pt-eager",
            "hf-pt-compile",
            "hf-ort",
            "ort-msft",
            "ort-convert-to-onnx",
        ],
    )
    parser.add_argument(
        "-m",
        "--model-name",
        type=str,
        required=True,
        help="Hugging Face name of model (e.g. 'meta-llama/Llama-2-7b-hf')",
    )
    parser.add_argument(
        "-a", "--auth", default=False, action="store_true", help="Use Hugging Face authentication token to access model"
    )

    # Args for choosing the model
    parser.add_argument(
        "-p",
        "--precision",
        required=True,
        type=str,
        default="fp32",
        choices=["int4", "int8", "fp16", "fp32"],
        help="Precision for model. For ONNX models, the model's precision should be set before running this script.",
    )
    parser.add_argument(
        "--hf-pt-dir-path",
        type=str,
        default="",
        help="Path to directory containing all PyTorch files (e.g. tokenizer, PyTorch model)",
    )
    parser.add_argument(
        "--hf-ort-dir-path",
        type=str,
        default="",
        help="Path to directory containing all ONNX files (e.g. tokenizer, decoder_merged, decoder, decoder_with_past)",
    )
    parser.add_argument(
        "--ort-model-path",
        type=str,
        default="",
        help="Path to ONNX model",
    )

    # Args for running and evaluating the model
    parser.add_argument(
        "-b",
        "--batch-sizes",
        default="1 2",
    )
    parser.add_argument(
        "-s",
        "--sequence-lengths",
        default="32 64 128 256 512",
    )
    parser.add_argument(
        "-d",
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        choices=["cpu", "cuda"],
    )
    parser.add_argument("-id", "--device-id", type=int, default=0)
    parser.add_argument("-w", "--warmup-runs", type=int, default=5)
    parser.add_argument("-n", "--num-runs", type=int, default=10)
    parser.add_argument("--seed", type=int, default=2)

    # Args for decoding logic
    parser.add_argument("--max-length", type=int, default=32)
    parser.add_argument("--num-return-sequences", type=int, default=1)

    # Args for accessing detailed info
    parser.add_argument("--profile", default=False, action="store_true")
    parser.add_argument(
        "--pt-filter-by", type=str, default="self_cpu_time_total", help="What to filter PyTorch profiler by"
    )
    parser.add_argument("--pt-num-rows", type=int, default=1000, help="Number of rows for PyTorch profiler to display")
    parser.add_argument("--verbose", default=False, action="store_true")
    parser.add_argument("--log-folder", type=str, default=os.path.join("."), help="Folder to cache log files")
    parser.add_argument(
        "--cache-dir",
        type=str,
        required=True,
        default="./model_cache",
        help="Cache dir where Hugging Face files are stored",
    )

    args = parser.parse_args()

    # Set seed properties
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    # Set runtime properties
    if "ort" in args.benchmark_type:
        setattr(args, "execution_provider", f"{args.device.upper()}ExecutionProvider")  # noqa: B010
        if args.execution_provider == "CUDAExecutionProvider":
            args.execution_provider = (args.execution_provider, {"device_id": rank})

    # Check that paths have been specified for any benchmarking with ORT
    if args.benchmark_type == "hf-ort":
        assert args.hf_ort_dir_path, "Please specify a path to `--hf-ort-dir-path`"
    if args.benchmark_type in {"ort-msft", "ort-convert-to-onnx"}:
        assert args.ort_model_path, "Please specify a path to `--ort-model-path`"

    args.batch_sizes = args.batch_sizes.split(" ")
    args.sequence_lengths = args.sequence_lengths.split(" ")

    # Use FP32 precision for FP32, INT8, INT4 CPU models, use FP16 precision for FP16 and INT4 GPU models
    args.precision = (
        "fp32" if args.precision in {"int8", "fp32"} or (args.precision == "int4" and args.device == "cpu") else "fp16"
    )

    # Check that only one (batch_size, sequence_length) combination is set for profiling
    if args.profile:
        assert len(args.batch_sizes) == 1 and len(args.sequence_lengths) == 1, (
            "Please provide only one (batch_size, sequence_length) combination for profiling"
        )

    return args


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b",
        "--batch-sizes",
        type=str,
        default="1 2",
    )

    parser.add_argument(
        "-s",
        "--sequence-lengths",
        type=str,
        default="8 16 32 64 128 256 512",
    )

    parser.add_argument(
        "-w",
        "--warmup-runs",
        type=int,
        default=5,
    )

    parser.add_argument(
        "-n",
        "--num-runs",
        type=int,
        default=1000,
    )

    parser.add_argument(
        "--hf-pt-eager",
        default=False,
        action="store_true",
        help="Benchmark in PyTorch without `torch.compile`",
    )

    parser.add_argument(
        "--hf-pt-compile",
        default=False,
        action="store_true",
        help="Benchmark in PyTorch with `torch.compile`",
    )

    parser.add_argument(
        "--hf-ort-dir-path",
        type=str,
        default="",
        help="Path to folder containing ONNX models for Optimum + ORT benchmarking",
    )

    parser.add_argument(
        "--ort-msft-model-path",
        type=str,
        default="",
        help="Path to ONNX model from https://github.com/microsoft/Llama-2-Onnx",
    )

    parser.add_argument(
        "--ort-convert-to-onnx-model-path",
        type=str,
        default="",
        help="Path to ONNX model from convert_to_onnx",
    )

    parser.add_argument(
        "--cache-dir",
        type=str,
        default="./model_cache",
        help="Cache dir where Hugging Face files are stored",
    )

    parser.add_argument(
        "--model-name",
        type=str,
        required=True,
        help="Model name in Hugging Face",
    )

    parser.add_argument(
        "--precision",
        type=str,
        required=True,
        choices=["int4", "int8", "fp16", "fp32"],
        help="Precision to run model",
    )

    parser.add_argument(
        "--device",
        type=str,
        required=True,
        choices=["cpu", "cuda"],
        help="Device to benchmark models",
    )

    parser.add_argument(
        "--device-id",
        type=int,
        default=0,
        help="GPU device ID",
    )

    parser.add_argument(
        "--verbose",
        default=False,
        action="store_true",
        help="Print detailed logs",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Number of mins to attempt the benchmark before moving on",
    )

    parser.add_argument(
        "--log-folder",
        type=str,
        default=None,
        help="Path to folder to save logs and results",
    )

    args = parser.parse_args()

    setattr(args, "model_size", args.model_name.split("/")[-1].replace(".", "-"))  # noqa: B010
    log_folder_name = f"./{args.model_size}_{args.precision}"
    if not args.log_folder:
        args.log_folder = log_folder_name
    os.makedirs(args.log_folder, exist_ok=True)

    # Convert timeout value to secs
    args.timeout *= 60

    return args


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-bt",
        "--benchmark-type",
        type=str,
        required=True,
        choices=["pt-eager", "pt-compile", "ort"],
    )

    parser.add_argument(
        "-m",
        "--model-name",
        type=str,
        required=False,
        help="Hugging Face name of model (e.g. 'meta-llama/Llama-2-7b-hf')",
    )

    parser.add_argument(
        "-a",
        "--auth",
        default=False,
        action="store_true",
        help="Use Hugging Face authentication token to access model",
    )

    parser.add_argument(
        "-t",
        "--trust",
        default=False,
        action="store_true",
        help="Whether or not to allow for custom models defined on the Hugging Face Hub in their own modeling files",
    )

    parser.add_argument(
        "-c",
        "--cache-dir",
        type=str,
        default=os.path.join(".", "model_cache"),
        help="Path to directory containing all Hugging Face files (e.g. config, tokenizer, PyTorch model). Use when loading model as `AutoModel.from_pretrained(model_name, cache_dir=cache_dir)`.",
    )

    parser.add_argument(
        "--hf-dir-path",
        type=str,
        default="",
        help="Path to directory containing all Hugging Face files (e.g. config, tokenizer, PyTorch model). Use when loading model as `AutoModel.from_pretrained(folder_path)`.",
    )

    parser.add_argument(
        "-o",
        "--onnx-model-path",
        required=False,
        help="Path to ONNX model",
    )

    parser.add_argument(
        "-f",
        "--prompts-file",
        required=True,
        default=os.path.join(".", "models", "llama", "prompts.json"),
        help="JSON file containing entries in the format 'prompt length: prompt' where prompt length = tokenized length of prompt",
    )

    parser.add_argument(
        "--use_buffer_share",
        default=False,
        action="store_true",
        help="Use when GroupQueryAttention (GQA) is in ONNX model",
    )

    (
        parser.add_argument(
            "--anomaly-filtering",
            default=False,
            action="store_true",
            help="Use this flag to filter anomaly accelerator times for tokens generated. \
              This may give more accurate latency and throughput metrics for tokens generated. \
              Wall-clock metrics are still reported with anomaly times though.",
        ),
    )

    parser.add_argument(
        "-b",
        "--batch-sizes",
        default="1 2",
    )

    parser.add_argument(
        "-s",
        "--prompt-lengths",
        default="16 64 256 1024",
    )

    parser.add_argument(
        "-p",
        "--precision",
        required=True,
        type=str,
        default="fp32",
        choices=["int4", "int8", "fp16", "fp32"],
        help="Precision for model. For ONNX models, the model's precision should be set before running this script.",
    )

    parser.add_argument(
        "-g",
        "--generation-length",
        type=int,
        default=256,
        help="Number of new tokens to generate",
    )

    parser.add_argument(
        "-d",
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        choices=["cpu", "cuda"],
    )

    parser.add_argument("-id", "--device-id", type=int, default=0)
    parser.add_argument("-w", "--warmup-runs", type=int, default=5)
    parser.add_argument("-n", "--num-runs", type=int, default=100)
    parser.add_argument("--seed", type=int, default=2)

    args = parser.parse_args()

    # Set seed properties
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    # Set runtime properties
    if "ort" in args.benchmark_type:
        setattr(args, "execution_provider", f"{args.device.upper()}ExecutionProvider")  # noqa: B010
        if args.execution_provider == "CUDAExecutionProvider":
            args.execution_provider = (args.execution_provider, {"device_id": args.device_id})

    # Check that paths have been specified for any benchmarking with ORT
    if args.benchmark_type == "ort":
        assert args.onnx_model_path, "Please specify a path to `--onnx-model-path`"

    args.batch_sizes = args.batch_sizes.split(" ")
    args.prompt_lengths = args.prompt_lengths.split(" ")

    # Use FP32 precision for FP32, INT8, INT4 CPU models, use FP16 precision for FP16 and INT4 GPU models
    setattr(args, "onnx_precision", args.precision)  # noqa: B010
    args.precision = (
        "fp32" if args.precision in {"int8", "fp32"} or (args.precision == "int4" and args.device == "cpu") else "fp16"
    )

    target_device = f"cuda:{args.device_id}" if args.device != "cpu" else args.device
    torch_dtype = torch.float16 if args.precision == "fp16" else torch.float32
    engine = "ort" if args.benchmark_type == "ort" else "pt"
    setattr(args, "target_device", target_device)  # noqa: B010
    setattr(args, "torch_dtype", torch_dtype)  # noqa: B010
    setattr(args, "engine", engine)  # noqa: B010
    setattr(args, "use_fp16", args.precision == "fp16")  # noqa: B010

    args.use_buffer_share = args.use_buffer_share and engine == "ort"

    return args


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--model_name",
        required=True,
        help="Model name in Hugging Face",
    )

    parser.add_argument(
        "-i",
        "--input",
        required=False,
        default=os.path.join("."),
        help="Directory path to PyTorch model and associated files if saved on disk, or ONNX model file location if optimize_optimum is passed.",
    )

    parser.add_argument(
        "-o",
        "--output",
        required=False,
        default=os.path.join(".", "llama_onnx_models"),
        help="Directory path to save exported model files in",
    )

    parser.add_argument(
        "-p",
        "--precision",
        required=False,
        type=Precision,
        default=Precision.FLOAT32,
        choices=[Precision.FLOAT32, Precision.FLOAT16, Precision.INT8, Precision.INT4],
        help="Precision to export model in",
    )

    parser.add_argument(
        "-e",
        "--execution_provider",
        required=False,
        default="cpu",
        choices=["cpu", "cuda"],
        help="Execution provider to verify parity with",
    )

    parser.add_argument(
        "-r",
        "--reexport",
        required=False,
        action="store_true",
        help="Re-export models and overwrite existing models in output folder",
    )
    parser.set_defaults(reexport=False)

    parser.add_argument(
        "--use_gqa",
        required=False,
        action="store_true",
        help="Use GroupQueryAttention instead of MultiHeadAttention",
    )
    parser.set_defaults(use_gqa=False)

    parser.add_argument(
        "--no_merged",
        required=False,
        action="store_true",
        help="Export models into 2 ONNX files instead of 1. Deprecated in favor of exporting into 1 ONNX file.",
    )
    parser.set_defaults(no_merged=False)

    parser.add_argument(
        "-q",
        "--quantization_method",
        default="",
        choices=["blockwise", "smooth_quant", "quantize_dynamic"],
        help="Run a specific quantization algorithm (blockwise for int4, smooth_quant for int8, quantize_dynamic for int8). Blockwise is recommended. Need to install extra packages in `requirements-quant.txt` for SmoothQuant.",
    )

    blockwise_group = parser.add_argument_group("blockwise (4-bit quantization)")

    parser.add_argument("--bits", default=4, type=int, help="the target bits to represent weight")

    blockwise_group.add_argument(
        "--block_size",
        required=False,
        default=32,
        type=int,
        help="Block size to quantize with. See https://github.com/microsoft/onnxruntime/blob/main/onnxruntime/python/tools/quantization/matmul_nbits_quantizer.py for details.",
    )

    blockwise_group.add_argument(
        "--int4_accuracy_level",
        required=False,
        type=int,
        help="Accuracy level of the 4-bit quantized MatMul computation. "
        "Refer to the MatMulNBits contrib op's 'accuracy_level' attribute for details "
        "(https://github.com/microsoft/onnxruntime/blob/main/docs/ContribOperators.md#commicrosoftmatmulnbits).",
    )

    smooth_quant_group = parser.add_argument_group("smooth_quant (8-bit quantization)")

    smooth_quant_group.add_argument(
        "--smooth_quant_alpha",
        required=False,
        default=0.8,
        type=float,
        help="Strength to control migration difficulty from activation to weights. Default is 0.8 to match value \
              used in original paper for LLaMA. Paper recommends using values in [0.4, 0.6] range. \
              Link to paper: https://arxiv.org/pdf/2211.10438.pdf",
    )

    smooth_quant_group.add_argument(
        "--smooth_quant_dataset",
        required=False,
        default="NeelNanda/pile-10k",
        help="Path to dataset for calibration during quantization",
    )

    smooth_quant_group.add_argument(
        "--pad_max",
        required=False,
        default=196,
        type=int,
        help="Max padding size",
    )

    smooth_quant_group.add_argument(
        "--calibration_sampling_size",
        required=False,
        type=int,
        default=8,
        help="Calibration sampling size for quantization config",
    )

    smooth_quant_group.add_argument(
        "--nc_workspace",
        required=False,
        type=str,
        default=os.path.join(".", "nc_workspace"),
        help="Workspace to save intermediate files generated by Intel's Neural Compressor package.",
    )

    quantize_dynamic_group = parser.add_argument_group("quantize_dynamic (8-bit quantization)")

    quantize_dynamic_group.add_argument(
        "--quantize_embedding_layer",
        required=False,
        action="store_true",
        help="Quantize MatMul, GEMM, and Gather.",
    )
    quantize_dynamic_group.set_defaults(quantize_embedding_layer=False)

    quantize_dynamic_group.add_argument(
        "--quantize_per_channel",
        required=False,
        action="store_true",
        help="Quantize weights per each channel.",
    )
    quantize_dynamic_group.set_defaults(quantize_per_channel=False)

    quantize_dynamic_group.add_argument(
        "--quantize_reduce_range",
        required=False,
        action="store_true",
        help="Quantize weights with 7 bits.",
    )
    quantize_dynamic_group.set_defaults(quantize_reduce_range=False)

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose logs",
    )
    parser.set_defaults(verbose=False)

    parser.add_argument(
        "-d",
        "--use_dynamo_export",
        action="store_true",
        help="Use the new Dynamo exporter instead of the old TorchScript exporter",
    )
    parser.set_defaults(use_dynamo_export=False)

    parser.add_argument(
        "--cache_dir",
        required=False,
        type=str,
        default="./model_cache",
        help="model cache dir to override default HF cache dir to avoid overflood the /home dir",
    )

    parser.add_argument(
        "--optimize_optimum",
        action="store_true",
        help="Avoid exporting model, only apply quantizations and optimizations to existing model exported from optimum.",
    )

    parser.add_argument(
        "--small_gpu",
        action="store_true",
        help="Load the llama in GPU every time for parity_check if it's running in a machine which GPU memory < 36GB.",
    )

    parser.set_defaults(optimize_optimum=False)

    args = parser.parse_args()
    return args


def get_args(argv: list[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--model_name",
        required=False,
        help="Model name in Hugging Face",
    )

    parser.add_argument(
        "-t",
        "--torch_model_directory",
        required=False,
        default=os.path.join("."),
        help="Path to folder containing PyTorch model and associated files if saved on disk",
    )

    parser.add_argument(
        "-o",
        "--onnx_model_path",
        required=True,
        default=os.path.join("."),
        help="Path to ONNX model (with external data files saved in the same folder as the model)",
    )

    parser.add_argument(
        "-ep",
        "--execution_provider",
        required=False,
        default="cpu",
        choices=["cpu", "cuda"],
        help="Execution provider to verify parity with",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose logs",
    )
    parser.set_defaults(verbose=False)

    parser.add_argument(
        "-p",
        "--use_past_kv",
        action="store_true",
        help="Use past key and past value as inputs to the model. Necessary for decoder_with_past_model.onnx models.",
    )
    parser.set_defaults(use_past_kv=False)

    parser.add_argument(
        "-g",
        "--use_buffer_share",
        action="store_true",
        help="Use if model has GroupQueryAttention and you want to enable past-present buffer sharing",
    )
    parser.set_defaults(use_buffer_share=False)

    parser.add_argument(
        "--merged",
        action="store_true",
        help="Use merged model (i.e. decoder_merged_model.onnx).",
    )
    parser.set_defaults(merged=False)

    parser.add_argument(
        "-fp",
        "--precision",
        required=True,
        choices=["int4", "int8", "fp16", "fp32"],
        help="Precision of model",
    )

    parser.add_argument(
        "--cache_dir",
        required=False,
        type=str,
        default="./model_cache",
        help="model cache dir to override default HF cache dir to avoid overflood the /home dir",
    )

    # The argument is used for CI mainly, because the CI machine has 24G GPU memory at most.
    parser.add_argument(
        "--small_gpu",
        action="store_true",
        help="Load the llama in GPU every time for parity_check if it's running in a machine which GPU memory < 36GB. ",
    )

    args = parser.parse_args() if argv == [] else parser.parse_args(argv)

    # Use FP32 precision for FP32, INT8, INT4 CPU models, use FP16 precision for FP16 and INT4 GPU models
    args.precision = (
        "fp32"
        if args.precision in {"int8", "fp32"} or (args.precision == "int4" and args.execution_provider == "cpu")
        else "fp16"
    )
    return args


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--audio-path",
        type=str,
        required=True,
        help="Path to folder of audio files for E2E evaluation",
    )

    parser.add_argument(
        "-l",
        "--language",
        default=None,
        help="Language of audio file",
    )

    parser.add_argument(
        "-t",
        "--task",
        default=None,
        choices=["transcribe", "translate"],
        help="Task to complete",
    )

    parser.add_argument(
        "-w",
        "--warmup-runs",
        type=int,
        default=5,
    )

    parser.add_argument(
        "-n",
        "--num-runs",
        type=int,
        default=10,
    )

    parser.add_argument(
        "--hf-pt-eager",
        default=False,
        action="store_true",
        help="Benchmark in PyTorch without `torch.compile`",
    )

    parser.add_argument(
        "--hf-pt-compile",
        default=False,
        action="store_true",
        help="Benchmark in PyTorch with `torch.compile`",
    )

    parser.add_argument(
        "--hf-ort-dir-path",
        type=str,
        help="Path to folder containing ONNX models for Optimum + ORT benchmarking",
    )

    parser.add_argument(
        "--ort-model-path",
        type=str,
        help="Path to ONNX model for ORT benchmarking",
    )

    parser.add_argument(
        "--model-name",
        type=str,
        required=True,
        help="Model name in Hugging Face (e.g. openai/whisper-large-v2)",
    )

    parser.add_argument(
        "--precision",
        type=str,
        required=True,
        choices=["int4", "int8", "fp16", "fp32"],
        help="Precision to run model",
    )

    parser.add_argument(
        "--device",
        type=str,
        required=True,
        choices=["cpu", "cuda"],
        help="Device to benchmark models",
    )

    parser.add_argument(
        "--device-id",
        type=int,
        default=0,
        help="GPU device ID",
    )

    parser.add_argument(
        "--verbose",
        default=False,
        action="store_true",
        help="Print detailed logs",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Number of mins to attempt the benchmark before moving on",
    )

    parser.add_argument(
        "--log-folder",
        type=str,
        default=None,
        help="Path to folder to save logs and results",
    )

    parser.add_argument("--tune", default=False, action="store_true")

    args = parser.parse_args()

    setattr(args, "model_size", args.model_name.split("/")[-1].replace(".", "-"))  # noqa: B010
    log_folder_name = f"./{args.model_size}-{args.precision}"
    if not args.log_folder:
        args.log_folder = log_folder_name
    os.makedirs(args.log_folder, exist_ok=True)

    # Convert timeout value to secs
    args.timeout *= 60

    return args


def get_args(builder: IRBuilder, rt_args: Sequence[RuntimeArg], line: int) -> ArgInfo:
    # The environment operates on Vars, so we make some up
    fake_vars = [(Var(arg.name), arg.type) for arg in rt_args]
    args = [
        builder.read(builder.add_local_reg(var, type, is_arg=True), line)
        for var, type in fake_vars
    ]
    arg_names = [
        arg.name if arg.kind.is_named() or (arg.kind.is_optional() and not arg.pos_only) else None
        for arg in rt_args
    ]
    arg_kinds = [arg.kind for arg in rt_args]
    return ArgInfo(args, arg_names, arg_kinds)


def get_args(type_spec: type) -> Union[NoneType, Tuple[type, ...]]:  # pylint: disable=g-bare-generic drop when 3.7 support is not needed
  """Call typing.get_args, with fallback for Python 3.7 and below."""
  if hasattr(typing, 'get_args'):
    return typing.get_args(type_spec)
  return getattr(type_spec, '__args__', NoneType)


import functools
import logging
import os
import pathlib
import re
import sys
from typing import Any, Callable

def parse_args(argv: Sequence[str] | None = None) -> dict[str, Any]:
    argv = sys.argv[1:] if argv is None else list(argv)
    remapped_deprecated_args = []
    for index, arg in enumerate(argv):
        if arg in DEPRECATED_SINGLE_DASH_ARGS:
            remapped_deprecated_args.append(arg)
            argv[index] = f"-{arg}"

    parser = _build_arg_parser()
    arguments = {key: value for key, value in vars(parser.parse_args(argv)).items() if value}
    if remapped_deprecated_args:
        arguments["remapped_deprecated_args"] = remapped_deprecated_args
    if "dont_order_by_type" in arguments:
        arguments["order_by_type"] = False
        del arguments["dont_order_by_type"]
    if "dont_follow_links" in arguments:
        arguments["follow_links"] = False
        del arguments["dont_follow_links"]
    if "dont_float_to_top" in arguments:
        del arguments["dont_float_to_top"]
        if arguments.get("float_to_top", False):
            sys.exit("Can't set both --float-to-top and --dont-float-to-top.")
        else:
            arguments["float_to_top"] = False
    multi_line_output = arguments.get("multi_line_output", None)
    if multi_line_output:
        if multi_line_output.isdigit():
            arguments["multi_line_output"] = WrapModes(int(multi_line_output))
        else:
            arguments["multi_line_output"] = WrapModes[multi_line_output]

    return arguments


def parse_args(args):  # noqa: D103
    arguments = vars(parser.parse_args(args=args or ["--help"]))
    if arguments["output"] != "plain" and arguments["error_format"]:
        raise parser.error(
            "--error-format can only be used with --output plain",
        )
    if arguments["output"] == "plain" and arguments["error_format"] is None:
        arguments["error_format"] = "{error.instance}: {error.message}\n"
    return arguments


def parse_args(args: Any) -> Any:
    return utils.structify(
        {
            "action": utils.get(args, str, "list", ["action"]),
            "agents": utils.get(args, list, [], ["agents"]),
            "configuration": utils.get(args, dict, {}, ["configuration"]),
            "environment": args.get("environment", args.get("name", None)),
            "episodes": utils.get(args, int, 1, ["episodes"]),
            "state": utils.get(args, dict, {}, ["state"]),
            "steps": utils.get(args, list, [], ["steps"]),
            "logs": utils.get(args, list, [], ["logs"]),
            "render": utils.get(args, dict, {"mode": "json"}, ["render"]),
            "display": utils.get(args, str, None, ["display"]),
            "debug": utils.get(args, bool, False, ["debug"]),
            "host": utils.get(args, str, "127.0.0.1", ["host"]),
            "port": utils.get(args, int, 8000, ["port"]),
            "in_path": utils.get(args, str, None, ["in"]),
            "out_path": utils.get(args, str, None, ["out"]),
            "log_path": utils.get(args, str, None, ["log"]),
            "info": utils.get(args, dict, {}, ["info"]),
        }
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Slug string")

    input_group = parser.add_argument_group(description="Input")
    input_group.add_argument("input_string", nargs='*',
                             help='Text to slugify')
    input_group.add_argument("--stdin", action='store_true',
                             help="Take the text from STDIN")

    parser.add_argument("--no-entities", action='store_false', dest='entities', default=True,
                        help="Do not convert HTML entities to unicode")
    parser.add_argument("--no-decimal", action='store_false', dest='decimal', default=True,
                        help="Do not convert HTML decimal to unicode")
    parser.add_argument("--no-hexadecimal", action='store_false', dest='hexadecimal', default=True,
                        help="Do not convert HTML hexadecimal to unicode")
    parser.add_argument("--max-length", type=int, default=0,
                        help="Output string length, 0 for no limit")
    parser.add_argument("--word-boundary", action='store_true', default=False,
                        help="Truncate to complete word even if length ends up shorter than --max_length")
    parser.add_argument("--save-order", action='store_true', default=False,
                        help="When set and --max_length > 0 return whole words in the initial order")
    parser.add_argument("--separator", type=str, default=DEFAULT_SEPARATOR,
                        help="Separator between words. By default " + DEFAULT_SEPARATOR)
    parser.add_argument("--stopwords", nargs='+',
                        help="Words to discount")
    parser.add_argument("--regex-pattern",
                        help="Python regex pattern for disallowed characters")
    parser.add_argument("--no-lowercase", action='store_false', dest='lowercase', default=True,
                        help="Activate case sensitivity")
    parser.add_argument("--replacements", nargs='+',
                        help="""Additional replacement rules e.g. "|->or", "%%->percent".""")
    parser.add_argument("--allow-unicode", action='store_true', default=False,
                        help="Allow unicode characters")

    args = parser.parse_args(argv[1:])

    if args.input_string and args.stdin:
        parser.error("Input strings and --stdin cannot work together")

    if args.replacements:
        def split_check(repl):
            SEP = '->'
            if SEP not in repl:
                parser.error("Replacements must be of the form: ORIGINAL{SEP}REPLACED".format(SEP=SEP))
            return repl.split(SEP, 1)
        args.replacements = [split_check(repl) for repl in args.replacements]

    if args.input_string:
        args.input_string = " ".join(args.input_string)
    elif args.stdin:
        args.input_string = sys.stdin.read()

    if not args.input_string:
        args.input_string = ''

    return args


def parse_args(args):
    parser = get_args_parser()
    parser.add_argument(
        "--use-env",
        "--use_env",
        default=False,
        action="store_true",
        help="Use environment variable to pass "
        "'local rank'. For legacy reasons, the default value is False. "
        "If set to True, the script will not pass "
        "--local-rank as argument, and will instead set LOCAL_RANK.",
    )
    return parser.parse_args(args)


def parse_args(args):
    parser = get_args_parser()
    return parser.parse_args(args)


def parse_args(
    *arg_descriptors: _ValueDescriptor,
) -> Callable[[Callable[_Concatenate[_U, _P], _T]], Callable[_Concatenate[_U, _P], _T]]:
    """A decorator which converts args from torch._C.Value to built-in types.

    For example:

    ```
    @parse_args('v', 'i', 'fs')
    foo(g, a, b, c):
        # a is torch._C.Value
        # b is int
        # c is list of floats
    ```

    Args:
        arg_descriptors: list of str, where each element is
            a string that specifies the type to convert to. Valid descriptors:
            "v": no conversion, keep torch._C.Value.
            "i": int
            "is": list of int
            "f": float
            "fs": list of float
            "b": bool
            "s": str
            "t": torch.Tensor
            "none": the variable is unused
    """

    def decorator(
        fn: Callable[_Concatenate[_U, _P], _T],
    ) -> Callable[_Concatenate[_U, _P], _T]:
        fn._arg_descriptors = arg_descriptors  # type: ignore[attr-defined]

        @functools.wraps(fn)
        def wrapper(g: _U, *args: _P.args, **kwargs: _P.kwargs) -> _T:
            # some args may be optional, so the length may be smaller
            FILE_BUG_MSG = (
                "If you believe this is not due to custom symbolic implementation within your code or "
                "an external library, please file an issue at "
                "https://github.com/pytorch/pytorch/issues/new?template=bug-report.yml to report this bug."
            )
            if len(arg_descriptors) < len(args):
                raise AssertionError(
                    f"A mismatch between the number of arguments ({len(args)}) and "
                    f"their descriptors ({len(arg_descriptors)}) was found at "
                    f"symbolic function '{fn.__name__}'. {FILE_BUG_MSG}"
                )

            try:
                sig = inspect.signature(fn)
                arg_names = list(sig.parameters.keys())[1:]
                fn_name = fn.__name__
            except Exception:
                # FIXME(justinchuby): Avoid catching Exception.
                # Catch a more specific exception instead.
                arg_names = [None] * len(args)  # type: ignore[list-item]
                fn_name = None
            # pyrefly: ignore [bad-assignment]
            args = [
                _parse_arg(arg, arg_desc, arg_name, fn_name)  # type: ignore[method-assign]
                for arg, arg_desc, arg_name in zip(args, arg_descriptors, arg_names)
            ]
            # only support _outputs in kwargs
            if len(kwargs) > 1:
                raise AssertionError(
                    f"Symbolic function {fn.__name__}'s '**kwargs' can contain a single "
                    f"key/value entry. "
                    f"{FILE_BUG_MSG}"
                )

            if len(kwargs) == 1:
                if "_outputs" not in kwargs:
                    raise AssertionError(
                        f"Symbolic function {fn.__name__}'s '**kwargs' can only contain "
                        f"'_outputs' key at '**kwargs'. "
                        f"{FILE_BUG_MSG}"
                    )
            return fn(g, *args, **kwargs)

        return wrapper

    return decorator


def parse_args():
    parser = argparse.ArgumentParser(
        description="""Blockwise FP4/NF4 quantization for MatMul 2D weight matrices.

A weight matrix is partitioned into blocks, where each block is a contiguous
subset inside the flattened transposed weight matrix. Each block is quantized
into a set of 4b integers with an absolute value scaling factor.
"""
    )

    parser.add_argument("--input_model", required=True, help="Path to the input model file")
    parser.add_argument("--output_model", required=True, help="Path to the output model file")
    parser.add_argument(
        "--quant_type",
        required=False,
        default=1,
        choices=[MatMulBnb4Quantizer.FP4, MatMulBnb4Quantizer.NF4],
        help="Quantization data type. 0: FP4, 1: NF4",
    )
    parser.add_argument(
        "--block_size",
        required=False,
        default=64,
        help="Block size for blockwise quantization. Note: bnb.nn.Linear4bit only uses block_size=64",
    )
    parser.add_argument("-v", "--verbose", required=False, action="store_true")
    parser.set_defaults(verbose=False)
    parser.add_argument(
        "--nodes_to_exclude",
        nargs="+",
        type=str,
        required=False,
        default=[],
        help="Specify the nodes to be excluded from quantization with node names",
    )

    return parser.parse_args()


def parse_args():
    parser = argparse.ArgumentParser(
        description="""Blockwise int4 quantization for MatMul 2D weight matrices.

A weight matrix is partitioned into into blocks, where each block is a
continguous subset inside each column. Each block is quantized into a
set of 4b integers with a scaling factor and an optional offset.
"""
    )

    parser.add_argument("--input_model", required=True, help="Path to the input model file")
    parser.add_argument("--output_model", required=True, help="Path to the output model file")
    parser.add_argument("--block_size", required=False, default=32, type=int, help="Block size for quantization")
    parser.add_argument(
        "--quant_method",
        default="default",
        type=str,
        choices=["default", "hqq", "rtn", "k_quant", "gptq", "nvidia_awq"],
        help="the algorithm used to quantize weight, \nrtn and gptq leverage Intel® Neural Compressor",
    )
    parser.add_argument("--bits", default=4, type=int, help="the target bits to represent weight")
    parser.add_argument(
        "--symmetric",
        required=False,
        default=True,
        const=True,
        nargs="?",
        type=ort_convert_str_to_bool,
        choices=[True, False],
        help="Indicate whether to quantize the model symmetrically, symmetric is not supported by hqq",
    )
    parser.add_argument(
        "--accuracy_level",
        required=False,
        type=int,
        help="Accuracy level of the 4-bit quantized MatMul computation. "
        "Refer to the MatMulNBits contrib op's 'accuracy_level' attribute for details "
        "(https://github.com/microsoft/onnxruntime/blob/main/docs/ContribOperators.md#commicrosoftmatmulnbits).",
    )
    parser.add_argument("-v", "--verbose", required=False, action="store_true")
    parser.set_defaults(verbose=False)
    parser.add_argument(
        "--nodes_to_exclude",
        nargs="+",
        type=str,
        required=False,
        default=[],
        help="Specify the nodes to be excluded from quantization with node names",
    )
    parser.add_argument(
        "--nodes_to_include",
        nargs="+",
        type=str,
        required=False,
        help="Specify the specific nodes to be included from quantization with node names",
    )
    parser.add_argument(
        "--quant_format",
        default="QOperator",
        type=str,
        choices=["QOperator", "QDQ"],
        help="QuantFormat {QOperator, QDQ}"
        "QOperator format quantizes the model with quantized operators directly."
        "QDQ format quantize the model by inserting DeQuantizeLinear before the MatMul.",
    )
    parser.add_argument(
        "--op_types_to_quantize",
        type=str,
        nargs="+",
        choices=["MatMul", "Gather"],
        help="op_types_to_quantize {MatMul, Gather}. Operators to quantize. Default is MatMul.",
    )
    parser.add_argument(
        "--quant_axes",
        type=parse_key_value_pair,
        nargs="+",
        required=False,
        help="Key-value pairs in op_type:axis_to_quantize separated by space."
        "Specify the axis to quantize for an op. Default {MatMul:0, Gather:1}"
        "Example: --quant_axes MatMul:0 Gather:1",
    )
    # Group arguments specific to nvidia_awq
    nv_awq_config = parser.add_argument_group("nvidia_awq", "Arguments specific to nvidia_awq quantization")
    nv_awq_config.add_argument(
        "--calib_dataset_name",
        type=str,
        default="cnn",
        help="Name of the calibration dataset for nvidia_awq.",
    )
    nv_awq_config.add_argument(
        "--tokenizer_dir",
        type=str,
        required=False,
        help="Path of the tokenizer dir.",
    )
    nv_awq_config.add_argument(
        "--calibration_method",
        type=str,
        required=False,
        choices=["awq", "awq_clip"],
        help="Support two options, awq implementation and weight clipping.",
    )
    nv_awq_config.add_argument(
        "--cache_dir",
        type=str,
        default="./cache",
        help="Cache directory for calibration data.",
    )
    return parser.parse_args()


def parse_args():
    parser = argparse.ArgumentParser(
        os.path.basename(__file__),
        description="""Convert the ONNX format model/s in the provided directory to ORT format models.
        All files with a `.onnx` extension will be processed. For each one, an ORT format model will be created in the
        given output directory, if specified, or the same directory.
        A configuration file will also be created containing the list of required operators for all
        converted models. This configuration file should be used as input to the minimal build via the
        `--include_ops_by_config` parameter.
        """,
    )

    parser.add_argument(
        "--output_dir",
        type=pathlib.Path,
        help="Provide an output directory for the converted model/s and configuration file. "
        "If unspecified, the converted ORT format model/s will be in the same directory as the ONNX model/s.",
    )

    parser.add_argument(
        "--optimization_style",
        nargs="+",
        default=[OptimizationStyle.Fixed.name, OptimizationStyle.Runtime.name],
        choices=[e.name for e in OptimizationStyle],
        help="Style of optimization to perform on the ORT format model. "
        "Multiple values may be provided. The conversion will run once for each value. "
        "The general guidance is to use models optimized with "
        f"'{OptimizationStyle.Runtime.name}' style when using NNAPI or CoreML and "
        f"'{OptimizationStyle.Fixed.name}' style otherwise. "
        f"'{OptimizationStyle.Fixed.name}': Run optimizations directly before saving the ORT "
        "format model. This bakes in any platform-specific optimizations. "
        f"'{OptimizationStyle.Runtime.name}': Run basic optimizations directly and save certain "
        "other optimizations to be applied at runtime if possible. This is useful when using a "
        "compiling EP like NNAPI or CoreML that may run an unknown (at model conversion time) "
        "number of nodes. The saved optimizations can further optimize nodes not assigned to the "
        "compiling EP at runtime.",
    )

    parser.add_argument(
        "--enable_type_reduction",
        action="store_true",
        help="Add operator specific type information to the configuration file to potentially reduce "
        "the types supported by individual operator implementations.",
    )

    parser.add_argument(
        "--custom_op_library",
        type=pathlib.Path,
        default=None,
        help="Provide path to shared library containing custom operator kernels to register.",
    )

    parser.add_argument(
        "--save_optimized_onnx_model",
        action="store_true",
        help="Save the optimized version of each ONNX model. "
        "This will have the same level of optimizations applied as the ORT format model.",
    )

    parser.add_argument(
        "--allow_conversion_failures",
        action="store_true",
        help="Whether to proceed after encountering model conversion failures.",
    )

    parser.add_argument(
        "--target_platform",
        type=str,
        default=None,
        choices=["arm", "amd64"],
        help="Specify the target platform where the exported model will be used. "
        "This parameter can be used to choose between platform-specific options, "
        "such as QDQIsInt8Allowed(arm), NCHWc (amd64) and NHWC (arm/amd64) format, different "
        "optimizer level options, etc.",
    )

    parser.add_argument(
        "model_path_or_dir",
        type=pathlib.Path,
        help="Provide path to ONNX model or directory containing ONNX model/s to convert. "
        "All files with a .onnx extension, including those in subdirectories, will be "
        "processed.",
    )

    parsed_args = parser.parse_args()
    parsed_args.optimization_style = [OptimizationStyle[style_str] for style_str in parsed_args.optimization_style]
    return parsed_args


def parse_args():
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(help="Command to execute", dest="cmd")

    extract_parser = sub_parsers.add_parser("extract", help="Extract embedded tuning results from an onnx file.")
    extract_parser.add_argument("input_onnx")
    extract_parser.add_argument("output_json")

    embed_parser = sub_parsers.add_parser("embed", help="Embed the tuning results into an onnx file.")
    embed_parser.add_argument("--force", "-f", action="store_true", help="Overwrite the tuning results if it existed.")
    embed_parser.add_argument("output_onnx", help="Path of the output onnx file.")
    embed_parser.add_argument("input_onnx", help="Path of the input onnx file.")
    embed_parser.add_argument("input_json", nargs="+", help="Path(s) of the tuning results file(s) to be embedded.")

    merge_parser = sub_parsers.add_parser("merge", help="Merge multiple tuning results files as a single one.")
    merge_parser.add_argument("output_json", help="Path of the output tuning results file.")
    merge_parser.add_argument("input_json", nargs="+", help="Paths of the tuning results files to be merged.")

    pprint_parser = sub_parsers.add_parser("pprint", help="Pretty print the tuning results.")
    pprint_parser.add_argument("json_or_onnx", help="A tuning results json file or an onnx file.")

    args = parser.parse_args()
    if len(vars(args)) == 0:
        parser.print_help()
        exit(-1)
    return args


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-bt",
        "--benchmark-type",
        type=str,
        required=True,
        choices=["hf-pt-eager", "hf-pt-compile", "hf-ort", "ort"],
    )

    parser.add_argument(
        "-m",
        "--model-name",
        type=str,
        required=True,
        help="Hugging Face name of model (e.g. 'openai/whisper-large-v2')",
    )
    parser.add_argument(
        "-p",
        "--precision",
        type=str,
        required=True,
        default="fp32",
        choices=["int4", "int8", "fp16", "fp32"],
        help="Precision for model. For ONNX models, the model's precision should be set before running this script.",
    )

    parser.add_argument(
        "--hf-pt-model-path",
        type=str,
        default="",
        help="Path to directory containing all PyTorch files (e.g. tokenizer, PyTorch model)",
    )
    parser.add_argument(
        "--hf-ort-dir-path",
        type=str,
        default="",
        help="Path to directory containing all ONNX files (e.g. tokenizer, encoder, decoder, decoder_with_past)",
    )
    parser.add_argument(
        "--ort-model-path",
        type=str,
        default="",
        help="Path to ONNX model",
    )

    # Args for running and evaluating the model
    parser.add_argument("-a", "--audio-path", type=str, required=True, help="Path to audio file for E2E evaluation")
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

    # Optional args:
    parser.add_argument("--sampling-rate", type=int, default=16000, help="Sampling rate for audio (in Hz)")

    # Args for decoding logic
    # Required args:
    parser.add_argument("--max-length", type=int, default=448)
    parser.add_argument("--min-length", type=int, default=0)
    parser.add_argument("--num-beams", type=int, default=1)
    parser.add_argument("--num-return-sequences", type=int, default=1)
    parser.add_argument("--length-penalty", type=float, default=1.0)
    parser.add_argument("--repetition-penalty", type=float, default=1.0)
    parser.add_argument("--no-repeat-ngram-size", type=int, default=3)

    # Optional args for E2E solution:
    parser.add_argument(
        "--decoder-input-ids",
        type=str,
        default="[]",
        help="The forced decoder ids for generation. Format is [start token, timestamp token, language token, task token]. Default is [start token]. See `decoder_input_ids` in https://github.com/microsoft/Olive/tree/main/examples/whisper for details.",
    )
    parser.add_argument(
        "--logits-processor",
        type=int,
        default=1,
        help="Whether to use timestamps logits processor or not (0 for false, 1 for true).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Temperature value for generation.",
    )

    # Args for accessing detailed info
    parser.add_argument("--profile", default=False, action="store_true")
    parser.add_argument(
        "--pt-filter-by", type=str, default="self_cpu_time_total", help="What to filter PyTorch profiler by"
    )
    parser.add_argument("--pt-num-rows", type=int, default=1000, help="Number of rows for PyTorch profiler to display")
    parser.add_argument("--verbose", default=False, action="store_true")
    parser.add_argument("--log-folder", type=str, default=os.path.join("."), help="Folder to cache log files")

    args = parser.parse_args()

    # Set seed properties
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    args.monitor_type = args.device
    # Set runtime properties
    if "ort" in args.benchmark_type:
        args.execution_provider = f"{args.device.upper()}ExecutionProvider"
        if args.execution_provider == "CUDAExecutionProvider":
            args.execution_provider = (args.execution_provider, {"device_id": args.device_id})

    # Check that model paths have been specified for any benchmarking with ORT
    if args.benchmark_type == "hf-ort":
        assert args.hf_ort_dir_path, "Please specify a path to `--hf-ort-dir-path`"
    if args.benchmark_type == "ort":
        assert args.ort_model_path, "Please specify a path to `--ort-model-path`"

    # Convert decoder_input_ids string to list of ids
    # (e.g. "[1, 50257]" for Hugging Face or "[50257]" for ORT)
    args.decoder_input_ids = ast.literal_eval(args.decoder_input_ids)

    return args


def parse_args():
    parser = argparse.ArgumentParser(
        os.path.basename(__file__), description="""Analyze an ONNX model for usage with the ORT mobile"""
    )

    parser.add_argument("--log_level", choices=["debug", "info"], default="info", help="Logging level")
    parser.add_argument(
        "--skip_optimize",
        action="store_true",
        help="Don't optimize the model to BASIC level prior to analyzing. "
        "Optimization will occur when exporting the model to ORT format, so in general "
        "should not be skipped unless you have a specific reason to do so.",
    )
    parser.add_argument("model_path", type=pathlib.Path, help="Provide path to ONNX model")

    return parser.parse_args()


def parse_args(line: str) -> list[str]:
    """Parse the first line of the program for the command line.

    This should have the form

      # cmd: mypy <options>

    For example:

      # cmd: mypy pkg/
    """
    m = re.match("# cmd: mypy (.*)$", line)
    if not m:
        return []  # No args; mypy will spit out an error.
    return m.group(1).split()


def parse_args(args: Sequence[str] | None) -> argparse.Namespace:
    """Parse input CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Parse one or more markdown files, "
        "convert each to HTML, and print to stdout",
        # NOTE: Remember to update README.md w/ the output of `markdown-it -h`
        epilog=(
            f"""
Interactive:

  $ markdown-it
  markdown-it-py [version {__version__}] (interactive)
  Type Ctrl-D to complete input, or Ctrl-C to exit.
  >>> # Example
  ... > markdown *input*
  ...
  <h1>Example</h1>
  <blockquote>
  <p>markdown <em>input</em></p>
  </blockquote>

Batch:

  $ markdown-it README.md README.footer.md > index.html
"""
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-v", "--version", action="version", version=version_str)
    parser.add_argument(
        "--stdin", action="store_true", help="read Markdown from standard input"
    )
    parser.add_argument(
        "filenames", nargs="*", help="specify an optional list of files to convert"
    )
    return parser.parse_args(args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Base random seed used to sample cards.",
    )
    parser.add_argument(
        "--num-hands",
        type=int,
        default=DEFAULT_NUM_HANDS,
        help="Number of hands to generate for each preset group.",
    )
    parser.add_argument(
        "--cards-per-hand",
        type=int,
        default=DEFAULT_CARDS_PER_HAND,
        help="Number of card chance actions to sample for each hand.",
    )
    parser.add_argument(
        "--num-presets",
        type=int,
        default=1,
        help="Number of preset hand groups to emit.",
    )
    parser.add_argument(
        "--deck-size",
        type=int,
        default=DEFAULT_DECK_SIZE,
        help="Size of the deck to sample from (expected 52 for standard hold'em).",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path(__file__).with_name("preset_hands.jsonl"),
        help="Output JSONL path. Defaults to preset_hands.jsonl in the same directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip confirming the OpenSpiel chance action range (pyspiel required).",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Logging verbosity.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level))
    return args


def parseArgs(args):
    """Parse argv.

    Returns:
        3-tuple (infile, axisLimits, options)
        axisLimits is either a Dict[str, Optional[float]], for pinning variation axes
        to specific coordinates along those axes (with `None` as a placeholder for an
        axis' default value); or a Dict[str, Tuple(float, float)], meaning limit this
        axis to min/max range.
        Axes locations are in user-space coordinates, as defined in the "fvar" table.
    """
    from fontTools import configLogger
    import argparse

    parser = argparse.ArgumentParser(
        "fonttools varLib.instancer",
        description="Partially instantiate a variable font",
    )
    parser.add_argument("input", metavar="INPUT.ttf", help="Input variable TTF file.")
    parser.add_argument(
        "locargs",
        metavar="AXIS=LOC",
        nargs="*",
        help="List of space separated locations. A location consists of "
        "the tag of a variation axis, followed by '=' and the literal, "
        "string 'drop', or colon-separated list of one to three values, "
        "each of which is the empty string, or a number. "
        "E.g.: wdth=100 or wght=75.0:125.0 or wght=100:400:700 or wght=:500: "
        "or wght=drop",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT.ttf",
        default=None,
        help="Output instance TTF file (default: INPUT-instance.ttf).",
    )
    parser.add_argument(
        "--static",
        dest="static",
        action="store_true",
        help="Make a static font: pin unspecified axes to their default location.",
    )
    parser.add_argument(
        "--no-optimize",
        dest="optimize",
        action="store_false",
        help="Don't perform IUP optimization on the remaining gvar TupleVariations",
    )
    parser.add_argument(
        "--no-overlap-flag",
        dest="overlap",
        action="store_false",
        help="Don't set OVERLAP_SIMPLE/OVERLAP_COMPOUND glyf flags (only applicable "
        "when generating a full instance)",
    )
    parser.add_argument(
        "--remove-overlaps",
        dest="remove_overlaps",
        action="store_true",
        help="Merge overlapping contours and components (only applicable "
        "when generating a full instance). Requires skia-pathops",
    )
    parser.add_argument(
        "--ignore-overlap-errors",
        dest="ignore_overlap_errors",
        action="store_true",
        help="Don't crash if the remove-overlaps operation fails for some glyphs.",
    )
    parser.add_argument(
        "--update-name-table",
        action="store_true",
        help="Update the instantiated font's `name` table. Input font must have "
        "a STAT table with Axis Value Tables",
    )
    parser.add_argument(
        "--downgrade-cff2",
        action="store_true",
        help="If all axes are pinned, downgrade CFF2 to CFF table format",
    )
    parser.add_argument(
        "--no-recalc-timestamp",
        dest="recalc_timestamp",
        action="store_false",
        help="Don't set the output font's timestamp to the current time.",
    )
    parser.add_argument(
        "--no-recalc-bounds",
        dest="recalc_bounds",
        action="store_false",
        help="Don't recalculate font bounding boxes",
    )
    loggingGroup = parser.add_mutually_exclusive_group(required=False)
    loggingGroup.add_argument(
        "-v", "--verbose", action="store_true", help="Run more verbosely."
    )
    loggingGroup.add_argument(
        "-q", "--quiet", action="store_true", help="Turn verbosity off."
    )
    options = parser.parse_args(args)

    if options.remove_overlaps:
        if options.ignore_overlap_errors:
            options.overlap = OverlapMode.REMOVE_AND_IGNORE_ERRORS
        else:
            options.overlap = OverlapMode.REMOVE
    else:
        options.overlap = OverlapMode(int(options.overlap))

    infile = options.input
    if not os.path.isfile(infile):
        parser.error("No such file '{}'".format(infile))

    configLogger(
        level=("DEBUG" if options.verbose else "ERROR" if options.quiet else "INFO")
    )

    try:
        axisLimits = parseLimits(options.locargs)
    except ValueError as e:
        parser.error(str(e))

    if len(axisLimits) != len(options.locargs):
        parser.error("Specified multiple limits for the same axis")

    return (infile, axisLimits, options)


def parse_args(
    argv: Sequence[str],
) -> tuple[finder.Plugins, argparse.Namespace]:
    """Procedure for parsing args, config, loading plugins."""
    prelim_parser = options.stage1_arg_parser()

    args0, rest = prelim_parser.parse_known_args(argv)
    # XXX (ericvw): Special case "forwarding" the output file option so
    # that it can be reparsed again for the BaseFormatter.filename.
    if args0.output_file:
        rest.extend(("--output-file", args0.output_file))

    flake8.configure_logging(args0.verbose, args0.output_file)

    cfg, cfg_dir = config.load_config(
        config=args0.config,
        extra=args0.append_config,
        isolated=args0.isolated,
    )

    plugin_opts = finder.parse_plugin_options(
        cfg,
        cfg_dir,
        enable_extensions=args0.enable_extensions,
        require_plugins=args0.require_plugins,
    )
    raw_plugins = finder.find_plugins(cfg, plugin_opts)
    plugins = finder.load_plugins(raw_plugins, plugin_opts)

    option_manager = manager.OptionManager(
        version=flake8.__version__,
        plugin_versions=plugins.versions_str(),
        parents=[prelim_parser],
        formatter_names=list(plugins.reporters),
    )
    options.register_default_options(option_manager)
    option_manager.register_plugins(plugins)

    opts = aggregator.aggregate_options(option_manager, cfg, cfg_dir, rest)

    for loaded in plugins.all_plugins():
        parse_options = getattr(loaded.obj, "parse_options", None)
        if parse_options is None:
            continue

        # XXX: ideally we wouldn't have two forms of parse_options
        try:
            parse_options(
                option_manager,
                opts,
                opts.filenames,
            )
        except TypeError:
            parse_options(opts)

    return plugins, opts


def parse_args():
    """Parse arguments."""
    help_description = """Bandit Config Generator

    This tool is used to generate an optional profile.  The profile may be used
    to include or skip tests and override values for plugins.

    When used to store an output profile, this tool will output a template that
    includes all plugins and their default settings.  Any settings which aren't
    being overridden can be safely removed from the profile and default values
    will be used.  Bandit will prefer settings from the profile over the built
    in values."""

    parser = argparse.ArgumentParser(
        description=help_description,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    if sys.version_info >= (3, 14):
        parser.suggest_on_error = True
        parser.color = False

    parser.add_argument(
        "--show-defaults",
        dest="show_defaults",
        action="store_true",
        help="show the default settings values for each "
        "plugin but do not output a profile",
    )
    parser.add_argument(
        "-o",
        "--out",
        dest="output_file",
        action="store",
        help="output file to save profile",
    )
    parser.add_argument(
        "-t",
        "--tests",
        dest="tests",
        action="store",
        default=None,
        type=str,
        help="list of test names to run",
    )
    parser.add_argument(
        "-s",
        "--skip",
        dest="skips",
        action="store",
        default=None,
        type=str,
        help="list of test names to skip",
    )
    args = parser.parse_args()

    if not args.output_file and not args.show_defaults:
        parser.print_help()
        parser.exit(1)

    return args


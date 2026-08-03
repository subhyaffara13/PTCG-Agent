import os

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="""Model optimizer and shape inferencer, in preparation for quantization,
Consists of three optional steps:
1. Symbolic shape inference (best for transformer models).
2. Model optimization.
3. ONNX shape inference.

Model quantization with QDQ format, i.e. inserting QuantizeLinear/DeQuantizeLinear on
the tensor, requires tensor shape information to perform its best. Currently, shape inferencing
works best with optimized model. As a result, it is highly recommended to run quantization
on optimized model with shape information. This is the tool for optimization and shape
inferencing.

Essentially this tool performs the following three (skippable) steps:

1. Symbolic shape inference.
2. Model optimization
3. ONNX shape inference"""
    )

    parser.add_argument("--input", required=True, help="Path to the input model file")
    parser.add_argument("--output", required=True, help="Path to the output model file")
    parser.add_argument(
        "--skip_optimization",
        type=bool,
        default=False,
        help="Skip model optimization step if true. It's a known issue that ORT"
        " optimization has difficulty with model size greater than 2GB, rerun with"
        " this option to get around this issue.",
    )
    parser.add_argument(
        "--skip_onnx_shape",
        type=bool,
        default=False,
        help="Skip ONNX shape inference. Symbolic shape inference is most effective"
        " with transformer based models. Skipping all shape inferences may"
        " reduce the effectiveness of quantization, as a tensor with unknown"
        " shape can not be quantized.",
    )
    parser.add_argument(
        "--skip_symbolic_shape",
        type=bool,
        default=False,
        help="Skip symbolic shape inference. Symbolic shape inference is most"
        " effective with transformer based models. Skipping all shape"
        " inferences may reduce the effectiveness of quantization, as a tensor"
        " with unknown shape can not be quantized.",
    )
    parser.add_argument(
        "--auto_merge",
        help="Automatically merge symbolic dims when confliction happens",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--int_max",
        help="maximum value for integer to be treated as boundless for ops like slice",
        type=int,
        default=2**31 - 1,
    )
    parser.add_argument(
        "--guess_output_rank",
        help="guess output rank to be the same as input 0 for unknown ops",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--verbose",
        help="Prints detailed logs of inference, 0: turn off, 1: warnings, 3: detailed",
        type=int,
        default=0,
    )
    parser.add_argument(
        "--save_as_external_data",
        help="Saving an ONNX model to external data",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--all_tensors_to_one_file",
        help="Saving all the external data to one file",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--external_data_location",
        help="The file location to save the external file",
        default=None,
    )
    parser.add_argument(
        "--external_data_size_threshold",
        help="The size threshold for external data",
        type=int,
        default=1024,
    )
    return parser.parse_args()


def parse_arguments():
    parser = argparse.ArgumentParser(description="The arguments for static quantization")
    parser.add_argument("-i", "--input_model_path", required=True, help="Path to the input onnx model")
    parser.add_argument(
        "-o", "--output_quantized_model_path", required=True, help="Path to the output quantized onnx model"
    )
    parser.add_argument(
        "--activation_type",
        choices=["qint8", "quint8", "qint16", "quint16", "qint4", "quint4", "qfloat8e4m3fn"],
        default="quint8",
        help="Activation quantization type used",
    )
    parser.add_argument(
        "--weight_type",
        choices=["qint8", "quint8", "qint16", "quint16", "qint4", "quint4", "qfloat8e4m3fn"],
        default="qint8",
        help="Weight quantization type used",
    )
    parser.add_argument("--enable_subgraph", action="store_true", help="If set, subgraph will be quantized.")
    parser.add_argument(
        "--force_quantize_no_input_check",
        action="store_true",
        help="By default, some latent operators like maxpool, transpose, do not quantize if their input is not"
        " quantized already. Setting to True to force such operator always quantize input and so generate"
        " quantized output. Also the True behavior could be disabled per node using the nodes_to_exclude.",
    )
    parser.add_argument(
        "--matmul_const_b_only",
        action="store_true",
        help="If set, only MatMul with const B will be quantized.",
    )
    parser.add_argument(
        "--add_qdq_pair_to_weight",
        action="store_true",
        help="If set, it remains floating-point weight and inserts both QuantizeLinear/DeQuantizeLinear"
        " nodes to weight.",
    )
    parser.add_argument(
        "--dedicated_qdq_pair",
        action="store_true",
        help="If set, it will create identical and dedicated QDQ pair for each node.",
    )
    parser.add_argument(
        "--op_types_to_exclude_output_quantization",
        nargs="+",
        default=[],
        help="If any op type is specified, it won't quantize the output of ops with this specific op types.",
    )
    parser.add_argument(
        "--calibration_method",
        default="minmax",
        choices=["minmax", "entropy", "percentile", "distribution"],
        help="Calibration method used",
    )
    parser.add_argument("--quant_format", default="qdq", choices=["qdq", "qoperator"], help="Quantization format used")
    parser.add_argument(
        "--calib_tensor_range_symmetric",
        action="store_true",
        help="If enabled, the final range of tensor during calibration will be explicitly"
        " set to symmetric to central point 0",
    )
    # TODO: --calib_strided_minmax"
    # TODO: --calib_moving_average_constant"
    # TODO: --calib_max_intermediate_outputs"
    parser.add_argument(
        "--calib_moving_average",
        action="store_true",
        help="If enabled, the moving average of"
        " the minimum and maximum values will be computed when the calibration method selected is MinMax.",
    )
    parser.add_argument(
        "--disable_quantize_bias",
        action="store_true",
        help="Whether to quantize floating-point biases by solely inserting a DeQuantizeLinear node"
        " If not set, it remains floating-point bias and does not insert any quantization nodes"
        " associated with biases.",
    )

    # TODO: Add arguments related to Smooth Quant

    parser.add_argument(
        "--use_qdq_contrib_ops",
        action="store_true",
        help="If set, the inserted QuantizeLinear and DequantizeLinear ops will have the com.microsoft domain,"
        " which forces use of ONNX Runtime's QuantizeLinear and DequantizeLinear contrib op implementations.",
    )
    parser.add_argument(
        "--minimum_real_range",
        type=float,
        default=0.0001,
        help="If set to a floating-point value, the calculation of the quantization parameters"
        " (i.e., scale and zero point) will enforce a minimum range between rmin and rmax. If (rmax-rmin)"
        " is less than the specified minimum range, rmax will be set to rmin + MinimumRealRange. This is"
        " necessary for EPs like QNN that require a minimum floating-point range when determining "
        " quantization parameters.",
    )
    parser.add_argument(
        "--qdq_keep_removable_activations",
        action="store_true",
        help="If set, removable activations (e.g., Clip or Relu) will not be removed,"
        " and will be explicitly represented in the QDQ model.",
    )
    parser.add_argument(
        "--qdq_disable_weight_adjust_for_int32_bias",
        action="store_true",
        help="If set, QDQ quantizer will not adjust the weight's scale when the bias"
        " has a scale (input_scale * weight_scale) that is too small.",
    )
    parser.add_argument("--per_channel", action="store_true", help="Whether using per-channel quantization")
    parser.add_argument(
        "--nodes_to_quantize",
        nargs="+",
        default=None,
        help="List of nodes names to quantize. When this list is not None only the nodes in this list are quantized.",
    )
    parser.add_argument(
        "--nodes_to_exclude",
        nargs="+",
        default=None,
        help="List of nodes names to exclude. The nodes in this list will be excluded from quantization when it is not None.",
    )
    parser.add_argument(
        "--op_per_channel_axis",
        nargs=2,
        action="append",
        metavar=("OP_TYPE", "PER_CHANNEL_AXIS"),
        default=[],
        help="Set channel axis for specific op type, for example: --op_per_channel_axis MatMul 1, and it's"
        " effective only when per channel quantization is supported and per_channel is True. If specific"
        " op type supports per channel quantization but not explicitly specified with channel axis,"
        " default channel axis will be used.",
    )
    parser.add_argument("--tensor_quant_overrides", help="Set the json file for tensor quantization overrides.")
    return parser.parse_args()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="The input model file")
    parser.add_argument("--output", help="The output model file")
    parser.add_argument(
        "--auto_merge",
        help="Automatically merge symbolic dims when confliction happens",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--int_max",
        help="maximum value for integer to be treated as boundless for ops like slice",
        type=int,
        default=2**31 - 1,
    )
    parser.add_argument(
        "--guess_output_rank",
        help="guess output rank to be the same as input 0 for unknown ops",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--verbose",
        help="Prints detailed logs of inference, 0: turn off, 1: warnings, 3: detailed",
        type=int,
        default=0,
    )
    parser.add_argument(
        "--save_as_external_data",
        help="Saving an ONNX model to external data",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--all_tensors_to_one_file",
        help="Saving all the external data to one file",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--external_data_location",
        help="The file location to save the external file",
        default="./",
    )
    parser.add_argument(
        "--external_data_size_threshold",
        help="The size threshold for external data",
        type=int,
        default=1024,
    )
    return parser.parse_args()


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--models",
        required=False,
        nargs="+",
        type=str,
        default=["bert-base-cased", "roberta-base", "gpt2"],
        choices=list(MODELS.keys()),
        help="Pre-trained models in the list: " + ", ".join(MODELS.keys()),
    )

    parser.add_argument(
        "--model_source",
        required=False,
        nargs=1,
        type=str,
        default="pt",
        choices=["pt", "tf"],
        help="Export onnx from pt or tf",
    )

    parser.add_argument(
        "--model_class",
        required=False,
        type=str,
        default=None,
        choices=list(MODEL_CLASSES),
        help="Model type selected in the list: " + ", ".join(MODEL_CLASSES),
    )

    parser.add_argument(
        "-e",
        "--engines",
        required=False,
        nargs="+",
        type=str,
        default=["onnxruntime"],
        choices=["onnxruntime", "torch", "torch2", "torchscript", "tensorflow"],
        help="Engines to benchmark",
    )

    parser.add_argument(
        "-c",
        "--cache_dir",
        required=False,
        type=str,
        default=os.path.join(".", "cache_models"),
        help="Directory to cache pre-trained models",
    )

    parser.add_argument(
        "--onnx_dir",
        required=False,
        type=str,
        default=os.path.join(".", "onnx_models"),
        help="Directory to store onnx models",
    )

    parser.add_argument("-g", "--use_gpu", required=False, action="store_true", help="Run on gpu device")

    parser.add_argument(
        "--provider",
        required=False,
        type=str,
        default=None,
        help="Execution provider to use",
    )

    parser.add_argument(
        "-p",
        "--precision",
        type=Precision,
        default=Precision.FLOAT32,
        choices=list(Precision),
        help="Precision of model to run. fp32 for full precision, fp16 for half precision, and int8 for quantization",
    )

    parser.add_argument("--verbose", required=False, action="store_true", help="Print more information")

    parser.add_argument(
        "--overwrite",
        required=False,
        action="store_true",
        help="Overwrite existing models",
    )

    parser.add_argument(
        "-o",
        "--optimizer_info",
        type=OptimizerInfo,
        default=OptimizerInfo.BYSCRIPT,
        choices=list(OptimizerInfo),
        help="Optimizer info: Use optimizer.py to optimize onnx model as default. Can also choose from by_ort and no_opt",
    )

    parser.add_argument(
        "-v",
        "--validate_onnx",
        required=False,
        action="store_true",
        help="Validate ONNX model",
    )

    parser.add_argument(
        "-f",
        "--fusion_csv",
        required=False,
        default=None,
        help="CSV file for saving summary results of graph optimization.",
    )

    parser.add_argument(
        "-d",
        "--detail_csv",
        required=False,
        default=None,
        help="CSV file for saving detail results.",
    )

    parser.add_argument(
        "-r",
        "--result_csv",
        required=False,
        default=None,
        help="CSV file for saving summary results.",
    )

    parser.add_argument(
        "-i",
        "--input_counts",
        required=False,
        nargs="+",
        default=[1],
        type=int,
        choices=[1, 2, 3],
        help="Number of ONNX model inputs. Please use 1 for fair comparison with Torch or TorchScript.",
    )

    parser.add_argument(
        "-t",
        "--test_times",
        required=False,
        default=100,
        type=int,
        help="Number of repeat times to get average inference latency.",
    )

    parser.add_argument("-b", "--batch_sizes", nargs="+", type=int, default=[1])

    parser.add_argument(
        "-s",
        "--sequence_lengths",
        nargs="+",
        type=int,
        default=[4, 8, 16, 32, 64, 128, 256],
    )

    parser.add_argument(
        "--disable_ort_io_binding",
        required=False,
        action="store_true",
        help="Disable running ONNX Runtime with binded inputs and outputs. ",
    )
    parser.set_defaults(disable_ort_io_binding=False)

    parser.add_argument(
        "-n",
        "--num_threads",
        required=False,
        nargs="+",
        type=int,
        default=[0],
        help="Threads to use",
    )

    parser.add_argument(
        "--force_num_layers",
        required=False,
        type=int,
        default=None,
        help="Manually set the model's layer number",
    )

    parser.add_argument(
        "--enable_arm64_bfloat16_fastmath_mlas_gemm",
        required=False,
        action="store_true",
        help="Enable bfloat16 mlas gemm kernels on aarch64. Supported only for CPU EP ",
    )
    parser.set_defaults(enable_arm64_bfloat16_fastmath_mlas_gemm=False)

    FusionOptions.add_arguments(parser)

    args = parser.parse_args()
    return args


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=str, help="bert onnx model path")

    parser.add_argument(
        "-b",
        "--batch_size",
        required=True,
        type=int,
        nargs="+",
        help="batch size of input. Allow one or multiple values in the range of [1, 128].",
    )

    parser.add_argument(
        "-s",
        "--sequence_length",
        required=True,
        type=int,
        help="maximum sequence length of input",
    )

    parser.add_argument(
        "--samples",
        required=False,
        type=int,
        default=10,
        help="number of samples to be generated",
    )

    parser.add_argument(
        "-t",
        "--test_times",
        required=False,
        type=int,
        default=0,
        help="number of times to run per sample. By default, the value is 1000 / samples",
    )

    parser.add_argument(
        "--opt_level",
        required=False,
        type=int,
        choices=[0, 1, 2, 3, 99],
        default=99,
        help="onnxruntime optimization level: 0 - disable all, 1 - basic, 2 - extended, 3 - layout, 99 - enable all.",
    )

    parser.add_argument(
        "--seed",
        required=False,
        type=int,
        default=3,
        help="random seed. Use the same seed to make sure test data is same in multiple tests.",
    )

    parser.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        help="print verbose information",
    )
    parser.set_defaults(verbose=False)

    parser.add_argument(
        "--log_severity",
        required=False,
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="0:Verbose, 1:Info, 2:Warning, 3:Error, 4:Fatal",
    )

    parser.add_argument("--use_gpu", required=False, action="store_true", help="use GPU")
    parser.set_defaults(use_gpu=False)

    parser.add_argument("--use_io_binding", required=False, action="store_true", help="use io_binding")
    parser.set_defaults(use_io_binding=False)

    parser.add_argument(
        "--provider",
        required=False,
        type=str,
        default=None,
        help="Execution provider to use",
    )

    parser.add_argument(
        "-n",
        "--intra_op_num_threads",
        required=False,
        type=int,
        default=None,
        help=">=0, set intra_op_num_threads",
    )

    parser.add_argument(
        "--input_ids_name",
        required=False,
        type=str,
        default=None,
        help="input name for input ids",
    )

    parser.add_argument(
        "--segment_ids_name",
        required=False,
        type=str,
        default=None,
        help="input name for segment ids",
    )

    parser.add_argument(
        "--input_mask_name",
        required=False,
        type=str,
        default=None,
        help="input name for attention mask",
    )

    parser.add_argument(
        "--input_tuning_results",
        default=None,
        type=str,
        help="tuning results (json) to be loaded before benchmark",
    )

    parser.add_argument(
        "--output_tuning_results",
        default=None,
        type=str,
        help="tuning results (json) to be saved after benchmark",
    )

    parser.add_argument(
        "-a",
        "--average_sequence_length",
        default=-1,
        type=int,
        help="average sequence length excluding padding",
    )

    parser.add_argument(
        "-r",
        "--random_sequence_length",
        required=False,
        action="store_true",
        help="use uniform random instead of fixed sequence length",
    )
    parser.set_defaults(random_sequence_length=False)

    parser.add_argument(
        "--mask_type",
        required=False,
        type=int,
        default=2,
        help="mask type: (1: mask index or sequence length, 2: raw 2D mask, 3: key len, cumulated lengths of query and key)",
    )

    args = parser.parse_args()
    return args


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--model", required=True, type=str, help="bert onnx model path.")

    parser.add_argument(
        "--output_dir",
        required=False,
        type=str,
        default=None,
        help="output test data path. Default is current directory.",
    )

    parser.add_argument("--batch_size", required=False, type=int, default=1, help="batch size of input")

    parser.add_argument(
        "--sequence_length",
        required=False,
        type=int,
        default=128,
        help="maximum sequence length of input",
    )

    parser.add_argument(
        "--input_ids_name",
        required=False,
        type=str,
        default=None,
        help="input name for input ids",
    )
    parser.add_argument(
        "--segment_ids_name",
        required=False,
        type=str,
        default=None,
        help="input name for segment ids",
    )
    parser.add_argument(
        "--input_mask_name",
        required=False,
        type=str,
        default=None,
        help="input name for attention mask",
    )

    parser.add_argument(
        "--samples",
        required=False,
        type=int,
        default=1,
        help="number of test cases to be generated",
    )

    parser.add_argument("--seed", required=False, type=int, default=3, help="random seed")

    parser.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        help="print verbose information",
    )
    parser.set_defaults(verbose=False)

    parser.add_argument(
        "--only_input_tensors",
        required=False,
        action="store_true",
        help="only save input tensors and no output tensors",
    )
    parser.set_defaults(only_input_tensors=False)

    parser.add_argument(
        "-a",
        "--average_sequence_length",
        default=-1,
        type=int,
        help="average sequence length excluding padding",
    )

    parser.add_argument(
        "-r",
        "--random_sequence_length",
        required=False,
        action="store_true",
        help="use uniform random instead of fixed sequence length",
    )
    parser.set_defaults(random_sequence_length=False)

    parser.add_argument(
        "--mask_type",
        required=False,
        type=int,
        default=2,
        help="mask type: (1: mask index, 2: raw 2D mask, 3: key lengths, cumulated lengths of query and key)",
    )

    args = parser.parse_args()
    return args


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline_model", required=True, type=str, help="baseline onnx model path.")

    parser.add_argument(
        "--optimized_model",
        required=True,
        type=str,
        default=None,
        help="path of the optimized model. It shall have same inputs as the baseline model.",
    )

    parser.add_argument(
        "--output_dir",
        required=False,
        type=str,
        default=None,
        help="output test data path. If not specified, test data will not be saved.",
    )

    parser.add_argument("--batch_size", required=True, type=int, help="batch size of input")

    parser.add_argument(
        "--sequence_length",
        required=True,
        type=int,
        help="maximum sequence length of input",
    )

    parser.add_argument("--rtol", required=False, type=float, default=1e-3, help="relative tolerance")

    parser.add_argument("--atol", required=False, type=float, default=1e-4, help="absolute tolerance")

    parser.add_argument(
        "--samples",
        required=False,
        type=int,
        default=100,
        help="number of test cases to be generated",
    )

    parser.add_argument("--seed", required=False, type=int, default=3, help="random seed")

    parser.add_argument("--use_gpu", required=False, action="store_true", help="use GPU")
    parser.set_defaults(use_gpu=False)

    parser.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        help="print verbose information",
    )
    parser.set_defaults(verbose=False)

    parser.add_argument(
        "--input_ids",
        required=False,
        type=str,
        default=None,
        help="input name for input ids",
    )
    parser.add_argument(
        "--segment_ids",
        required=False,
        type=str,
        default=None,
        help="input name for segment ids",
    )
    parser.add_argument(
        "--input_mask",
        required=False,
        type=str,
        default=None,
        help="input name for attention mask",
    )

    parser.add_argument(
        "--mask_type",
        required=False,
        type=int,
        default=2,
        help="mask type: (1: mask index or sequence length, 2: raw 2D mask, 3: key len, cumulated lengths of query and key)",
    )

    args = parser.parse_args()
    return args


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse arguments

    Args:
        argv (Optional[List[str]], optional): _description_. Defaults to None.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser()

    input_group = parser.add_argument_group("Input options")

    input_group.add_argument(
        "-m",
        "--model_name_or_path",
        required=True,
        type=str,
        help="Pytorch model checkpoint path, or pretrained model name in the list: "
        + ", ".join(PRETRAINED_GPT2_MODELS + PRETRAINED_T5_MODELS + PRETRAINED_MT5_MODELS),
    )

    input_group.add_argument(
        "--model_type",
        required=False,
        type=str,
        default="gpt2",
        choices=["gpt2", "t5", "mt5"],
        help="Model type (default is gpt2) in the list: " + ", ".join(["gpt2", "t5", "mt5"]),
    )

    input_group.add_argument(
        "--cache_dir",
        required=False,
        type=str,
        default=os.path.join(".", "cache_models"),
        help="Directory to cache pre-trained models",
    )

    input_group.add_argument(
        "--decoder_onnx",
        required=False,
        type=str,
        default="",
        help="Path of onnx model for decoder. Specify it when you have exported the model.",
    )

    input_group.add_argument(
        "--encoder_decoder_init_onnx",
        required=False,
        type=str,
        default="",
        help="Path of ONNX model for encoder and decoder initialization. Specify it when you have exported the model.",
    )

    parser.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        help="Print more information",
    )
    parser.set_defaults(verbose=False)

    output_group = parser.add_argument_group("Output options")

    output_group.add_argument(
        "--output",
        required=True,
        type=str,
        help="Output path for onnx model with beam search.",
    )

    output_group.add_argument(
        "-p",
        "--precision",
        required=False,
        type=str,
        default=Precision.FLOAT32.value,
        choices=[Precision.FLOAT32.value, Precision.FLOAT16.value],
        help="Precision of model to run. fp32 for full precision, fp16 for half or mixed precision",
    )

    output_group.add_argument(
        "-b",
        "--op_block_list",
        required=False,
        nargs="*",
        default=["auto"],
        help="Disable certain onnx operators when exporting model to onnx format. When using default"
        'value for gpt2 type of model fp16 precision, it will be set to ["Add", "LayerNormalization",'
        ' "SkipLayerNormalization", "FastGelu"]. Other situation, it will be set to []',
    )

    output_group.add_argument(
        "-e",
        "--use_external_data_format",
        required=False,
        action="store_true",
        help="save external data for model > 2G",
    )
    output_group.set_defaults(use_external_data_format=False)

    output_group.add_argument(
        "-s",
        "--run_shape_inference",
        required=False,
        action="store_true",
        help="run shape inference",
    )
    output_group.set_defaults(run_shape_inference=False)

    output_group.add_argument(
        "-dpvs",
        "--disable_pad_vocab_size",
        required=False,
        action="store_true",
        help="Do not pad logits MatMul weight to be a multiple of 8 along the dimension where dim value is"
        " the vocab size. The logits MatMul may hence be of poor performance for fp16 precision.",
    )
    output_group.set_defaults(disable_pad_vocab_size=False)

    output_group.add_argument(
        "-dsgd",
        "--disable_separate_gpt2_decoder_for_init_run",
        required=False,
        action="store_true",
        help="Do not create separate decoder subgraphs for initial and remaining runs. This does not allow "
        "for optimizations based on sequence lengths in each subgraph",
    )
    output_group.set_defaults(disable_separate_gpt2_decoder_for_init_run=False)

    output_group.add_argument(
        "-i",
        "--disable_shared_initializers",
        required=False,
        action="store_true",
        help="do not share initializers in encoder and decoder for T5 or in the init decoder and decoder for "
        "GPT2. It will increase memory usage of t5/mt5/gpt2 models.",
    )
    output_group.set_defaults(disable_shared_initializers=False)

    output_group.add_argument(
        "--encoder_decoder_init",
        required=False,
        action="store_true",
        help="Add decoder initialization to encoder for T5 model. This is legacy format that will be deprecated.",
    )
    output_group.set_defaults(encoder_decoder_init=False)

    model_group = parser.add_argument_group("Beam search parameters that stored in the output model")

    model_group.add_argument(
        "--output_sequences_scores",
        required=False,
        action="store_true",
        help="output sequences scores",
    )
    model_group.set_defaults(output_sequences_scores=False)

    model_group.add_argument(
        "--output_token_scores",
        required=False,
        action="store_true",
        help="output token scores",
    )
    model_group.set_defaults(output_token_scores=False)

    model_group.add_argument("--early_stopping", required=False, action="store_true")
    model_group.set_defaults(early_stopping=False)

    model_group.add_argument(
        "--no_repeat_ngram_size",
        type=int,
        required=False,
        default=0,
        help="No repeat ngram size",
    )

    model_group.add_argument(
        "--vocab_mask",
        required=False,
        action="store_true",
        help="Enable vocab_mask. This mask applies only to every generated token to filter some bad words.",
    )
    model_group.set_defaults(vocab_mask=False)

    model_group.add_argument(
        "--past_present_share_buffer",
        required=False,
        action="store_true",
        help="Use shared buffer for past and present, currently work for gpt2 greedy/sampling search.",
    )
    model_group.set_defaults(past_present_share_buffer=False)

    model_group.add_argument(
        "--use_decoder_masked_attention",
        required=False,
        action="store_true",
        help="Uses `DecoderMaskedSelfAttention` or `DecoderMaskedMultiHeadAttention` to optimize the decoding Attention computation. "
        "Must be used with `past_present_share_buffer`. Currently, only Attention head sizes of 32, 64 and 128 are supported.",
    )
    model_group.set_defaults(use_decoder_masked_attention=False)

    model_group.add_argument(
        "--prefix_vocab_mask",
        required=False,
        action="store_true",
        help="Enable prefix_vocab_mask. This mask can be used to filter bad words in the first generated token only",
    )
    model_group.set_defaults(prefix_vocab_mask=False)

    model_group.add_argument(
        "--custom_attention_mask",
        required=False,
        action="store_true",
        help="Enable custom_attention_mask. This mask can be used to replace default encoder attention mask",
    )
    model_group.set_defaults(custom_attention_mask=False)

    model_group.add_argument(
        "--presence_mask",
        required=False,
        action="store_true",
        help="Presence mask for custom sampling",
    )
    model_group.set_defaults(presence_mask=False)

    model_group.add_argument(
        "--seed",
        required=False,
        action="store_true",
        help="Random seed for sampling op",
    )
    model_group.set_defaults(seed=False)

    beam_parameters_group = parser.add_argument_group(
        "Beam search parameters not stored in the output model, for testing parity and performance"
    )

    beam_parameters_group.add_argument("--min_length", type=int, required=False, default=1, help="Min sequence length")

    beam_parameters_group.add_argument("--max_length", type=int, required=False, default=50, help="Max sequence length")

    beam_parameters_group.add_argument("--num_beams", type=int, required=False, default=4, help="Beam size")

    beam_parameters_group.add_argument(
        "--num_return_sequences",
        type=int,
        required=False,
        default=1,
        help="Number of return sequence <= num_beams",
    )

    beam_parameters_group.add_argument(
        "--length_penalty",
        type=float,
        required=False,
        default=1,
        help="Positive. >1 to penalize and <1 to encourage short sentence.",
    )

    beam_parameters_group.add_argument(
        "--repetition_penalty",
        type=float,
        required=False,
        default=1,
        help="Positive. >1 to penalize and <1 to encourage.",
    )

    beam_parameters_group.add_argument(
        "--temperature",
        type=float,
        required=False,
        default=1.0,
        help="The value used to module the next token probabilities.",
    )

    beam_parameters_group.add_argument(
        "--top_p",
        type=float,
        required=False,
        default=1.0,
        help="Top P for sampling",
    )

    beam_parameters_group.add_argument(
        "--filter_value",
        type=float,
        required=False,
        default=-float("Inf"),
        help="Filter value for Top P sampling",
    )

    beam_parameters_group.add_argument(
        "--min_tokens_to_keep",
        type=int,
        required=False,
        default=1,
        help="Minimum number of tokens we keep per batch example in the output.",
    )

    beam_parameters_group.add_argument(
        "--presence_penalty",
        type=float,
        required=False,
        default=0.0,
        help="presence penalty for custom sampling.",
    )

    beam_parameters_group.add_argument(
        "--custom",
        type=int,
        required=False,
        default=0,
        help="If 1 customized top P logic is applied",
    )

    beam_parameters_group.add_argument(
        "--vocab_size",
        type=int,
        required=False,
        default=-1,
        help="Vocab_size of the underlying model used to decide the shape of vocab mask",
    )

    beam_parameters_group.add_argument(
        "--eos_token_id",
        type=int,
        required=False,
        default=-1,
        help="custom eos_token_id for generating model with existing onnx encoder/decoder",
    )

    beam_parameters_group.add_argument(
        "--pad_token_id",
        type=int,
        required=False,
        default=-1,
        help="custom pad_token_id for generating model with existing onnx encoder/decoder",
    )

    test_group = parser.add_argument_group("Other options for testing parity and performance")

    test_group.add_argument(
        "--use_sln_strict_mode",
        required=False,
        action="store_true",
        help="Enable strict mode for SLN in CUDA provider. This ensures a better accuracy but will be slower.",
    )
    test_group.set_defaults(use_sln_strict_mode=False)

    test_group.add_argument(
        "--use_gpu",
        required=False,
        action="store_true",
        help="use GPU for inference. Required for fp16.",
    )
    test_group.set_defaults(use_gpu=False)

    test_group.add_argument(
        "--disable_parity",
        required=False,
        action="store_true",
        help="do not run parity test",
    )
    test_group.set_defaults(disable_parity=False)

    test_group.add_argument(
        "--disable_perf_test",
        required=False,
        action="store_true",
        help="do not run perf test",
    )
    test_group.set_defaults(disable_perf_test=False)

    test_group.add_argument(
        "--torch_performance",
        required=False,
        action="store_true",
        help="test PyTorch performance",
    )
    test_group.set_defaults(torch_performance=False)

    test_group.add_argument(
        "--total_runs",
        required=False,
        type=int,
        default=1,
        help="Number of times of inference for latency measurement",
    )

    test_group.add_argument(
        "--save_test_data",
        required=False,
        action="store_true",
        help="save test data for onnxruntime_perf_test tool",
    )
    test_group.set_defaults(save_test_data=False)

    args = parser.parse_args(argv)

    return args


def parse_arguments():
    """arguments parsing."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--model",
        required=True,
        type=str,
        default=["meta-llama/Llama-2-70b-hf"],
        help="Pre-trained models in huggingface model hub",
    )
    parser.add_argument(
        "-s",
        "--saved_path",
        required=False,
        type=str,
        default="./onnx_models/",
        help="where the onnx model will be saved",
    )
    parser.add_argument(
        "--cache_dir",
        required=False,
        type=str,
        default=None,
        help=("cache directly of huggingface, by setting this to avoid useless downloading if you have one"),
    )
    parser.add_argument(
        "--with_past",
        action="store_true",
        default=False,
        help=("The tool will export onnx without past-key-value by default"),
    )
    parser.add_argument(
        "--opset",
        required=False,
        type=int,
        default=17,
        help=(
            "the opset to save onnx model, \
              try to increase it if this opset doens't have new features you want"
        ),
    )
    return parser.parse_args()


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--silent",
        required=False,
        action="store_true",
        help="Do not print error message",
    )
    parser.set_defaults(silent=False)

    args = parser.parse_args()
    return args


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        required=False,
        type=str,
        help="Set the input file for reading the profile results",
    )

    parser.add_argument(
        "-m",
        "--model",
        required=False,
        type=str,
        help="onnx model path to run profiling. Required when --input is not specified.",
    )

    parser.add_argument(
        "-b",
        "--batch_size",
        required=False,
        type=int,
        default=1,
        help="batch size of input",
    )

    parser.add_argument(
        "-s",
        "--sequence_length",
        required=False,
        type=int,
        default=32,
        help="sequence length of input",
    )

    parser.add_argument(
        "--past_sequence_length",
        required=False,
        type=int,
        default=1,
        help="past sequence length for gpt2",
    )

    parser.add_argument(
        "--global_length",
        required=False,
        type=int,
        default=1,
        help="number of global tokens for longformer",
    )

    parser.add_argument(
        "--samples",
        required=False,
        type=int,
        default=1000,
        help="number of samples to test. Set it large enough to reduce the variance of performance result.",
    )

    parser.add_argument(
        "--threshold",
        required=False,
        type=float,
        default=0.01,
        help="Threshold of run time ratio among all nodes. Nodes with larger ratio will show in top expensive nodes.",
    )

    parser.add_argument(
        "--thread_num",
        required=False,
        type=int,
        default=-1,
        help="number of threads to use",
    )

    parser.add_argument(
        "--input_ids_name",
        required=False,
        type=str,
        default=None,
        help="input name for input IDs, for bert",
    )
    parser.add_argument(
        "--segment_ids_name",
        required=False,
        type=str,
        default=None,
        help="input name for segment IDs, for bert",
    )
    parser.add_argument(
        "--input_mask_name",
        required=False,
        type=str,
        default=None,
        help="input name for attention mask, for bert",
    )

    parser.add_argument(
        "--dummy_inputs",
        required=False,
        default="default",
        choices=["bert", "gpt2", "longformer", "default"],
        help="Type of model inputs. The default will create dummy inputs with ones.",
    )

    parser.add_argument("-g", "--use_gpu", required=False, action="store_true", help="use GPU")
    parser.set_defaults(use_gpu=False)

    parser.add_argument(
        "--provider",
        required=False,
        type=str,
        default="cuda",
        help="Execution provider to use",
    )

    parser.add_argument(
        "--basic_optimization",
        required=False,
        action="store_true",
        help="Enable only basic graph optimizations. By default, all optimizations are enabled in OnnxRuntime",
    )
    parser.set_defaults(basic_optimization=False)

    parser.add_argument(
        "--kernel_time_only",
        required=False,
        action="store_true",
        help="Only include the kernel time and no fence time",
    )
    parser.set_defaults(kernel_time_only=False)

    parser.add_argument("-v", "--verbose", required=False, action="store_true")
    parser.set_defaults(verbose=False)

    return parser.parse_args(argv)


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        required=False,
        type=str,
        help="Set the input file for reading the profile results",
    )

    parser.add_argument(
        "--threshold",
        required=False,
        type=float,
        default=0.01,
        help="Threshold of run time ratio among all nodes. Nodes with larger ratio will show in top expensive nodes.",
    )

    parser.add_argument(
        "--provider",
        required=False,
        type=str,
        default="cuda",
        help="Execution provider to use",
    )

    parser.add_argument(
        "--kernel_time_only",
        required=False,
        action="store_true",
        help="Only include the kernel time and no fence time",
    )

    parser.set_defaults(kernel_time_only=False)

    parser.add_argument("-v", "--verbose", required=False, action="store_true")
    parser.set_defaults(verbose=False)

    return parser.parse_args(argv)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=str)
    parser.add_argument("--output", required=True, type=str)
    parser.add_argument("--input_ids", required=True, type=str)
    parser.add_argument("--segment_ids", required=True, type=str)
    parser.add_argument("--input_mask", required=True, type=str)
    parser.add_argument("--output_names", required=False, type=str, default=None)
    parser.add_argument("--batch_size", required=False, type=int, default=1)
    parser.add_argument("--sequence_length", required=False, type=int, default=128)
    parser.add_argument("--enable_shape_opt", required=False, action="store_true")
    parser.set_defaults(enable_shape_opt=False)
    parser.add_argument("--enable_reshape_opt", required=False, action="store_true")
    parser.set_defaults(enable_reshape_opt=False)
    parser.add_argument("--verbose", required=False, action="store_true")
    parser.set_defaults(verbose=False)
    args = parser.parse_args()
    return args


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--model_name",
        required=False,
        type=str,
        default=PRETRAINED_SQUAD_MODELS[0],
        help=f"Checkpoint directory or pre-trained model names in the list: {PRETRAINED_SQUAD_MODELS}",
    )

    parser.add_argument(
        "-s",
        "--sequence_lengths",
        nargs="+",
        type=int,
        default=[384],
        help="Sequence lengths for onnx model inputs. It could have multiple values.",
    )

    parser.add_argument(
        "-b",
        "--batch_size",
        type=int,
        default=1,
        help="batch size for inference.",
    )

    parser.add_argument("-t", "--total", type=int, default=0, help="Total samples to test. 0 means all samples.")

    parser.add_argument(
        "--onnx",
        required=False,
        type=str,
        default=None,
        help="Optional onnx model path. If not specified, optimum will be used to export onnx model for testing.",
    )

    parser.add_argument(
        "--provider",
        required=False,
        default="CUDAExecutionProvider",
        help="Select which Execution Provider to use for runs. Default is CUDAExecutionProvider.",
    )

    parser.add_argument("--use_io_binding", required=False, action="store_true", help="Use IO Binding for GPU.")
    parser.set_defaults(use_io_binding=False)

    args = parser.parse_args(argv)

    return args


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--model_name_or_path",
        required=True,
        type=str,
        help="Model path, or pretrained model name selected in the list: " + ", ".join(PRETRAINED_GPT2_MODELS),
    )

    parser.add_argument(
        "--model_class",
        required=False,
        type=str,
        default="GPT2LMHeadModel",
        choices=list(MODEL_CLASSES.keys()),
        help="Model type selected in the list: " + ", ".join(MODEL_CLASSES.keys()),
    )

    parser.add_argument(
        "--cache_dir",
        required=False,
        type=str,
        default=os.path.join(".", "cache_models"),
        help="Directory to cache pre-trained models",
    )

    parser.add_argument(
        "--onnx_dir",
        required=False,
        type=str,
        default=os.path.join(".", "onnx_models"),
        help="Directory to store onnx models",
    )

    parser.add_argument(
        "--test_times",
        required=False,
        default=100,
        type=int,
        help="Number of repeat times to get average inference latency.",
    )

    parser.add_argument(
        "-v",
        "--validate_onnx",
        required=False,
        action="store_true",
        help="Validate ONNX model",
    )

    parser.add_argument(
        "-o",
        "--optimize_onnx",
        required=False,
        action="store_true",
        help="Use optimizer.py to optimize onnx model",
    )
    parser.set_defaults(optimize_onnx=False)

    parser.add_argument(
        "--stage",
        type=int,
        default=0,
        required=False,
        choices=[0, 1, 2],
        help="Stage in generation: 1 (initial decoder), 2 (decoder), 0 (both). "
        "1 - decode the first token when past_sequence_length is zero; "
        "2 - decode the remaining tokens when past_sequence_length is not zero; "
        "0 - one onnx model for both stages 1 and 2. "
        "Note that we will optimize 1 and 2 differently for best performance.",
    )

    parser.add_argument("--use_gpu", required=False, action="store_true", help="use GPU for inference")
    parser.set_defaults(use_gpu=False)

    parser.add_argument(
        "-p",
        "--precision",
        type=Precision,
        default=Precision.FLOAT32,
        choices=list(Precision),
        help="Precision of model to run. fp32 for full precision, fp16 for half precision, and int8 for quantization",
    )

    parser.add_argument("--torchscript", required=False, action="store_true", help="use Torchscript")
    parser.set_defaults(torchscript=False)

    parser.add_argument("-b", "--batch_sizes", nargs="+", type=int, default=[1], help="batch size")

    parser.add_argument(
        "--sequence_lengths",
        nargs="+",
        type=int,
        default=[1],
        help="sequence lengths (excluding past)",
    )

    parser.add_argument(
        "-s",
        "--past_sequence_lengths",
        nargs="+",
        type=int,
        default=[8, 16, 32, 64, 128, 256],
        help="past sequence lengths",
    )

    parser.add_argument(
        "-r",
        "--result_csv",
        required=False,
        default=None,
        help="CSV file for saving summary results.",
    )

    parser.add_argument("--thread_num", required=False, type=int, default=-1, help="Threads to use")

    parser.add_argument("--include_copy_output_latency", required=False, action="store_true")
    parser.set_defaults(include_copy_output_latency=False)

    parser.add_argument("--verbose", required=False, action="store_true")
    parser.set_defaults(verbose=False)

    parser.add_argument("--output_torch_latency", required=False, action="store_true")
    parser.set_defaults(output_torch_latency=False)

    parser.add_argument("--disable_io_binding", required=False, action="store_true")
    parser.set_defaults(disable_io_binding=False)

    args = parser.parse_args(argv)

    return args


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--model_name_or_path",
        required=True,
        type=str,
        help="Model path, or pretrained model name in the list: " + ", ".join(PRETRAINED_GPT2_MODELS),
    )

    parser.add_argument(
        "--model_class",
        required=False,
        type=str,
        default="GPT2LMHeadModel",
        choices=list(MODEL_CLASSES.keys()),
        help="Model type selected in the list: " + ", ".join(MODEL_CLASSES.keys()),
    )

    parser.add_argument(
        "--cache_dir",
        required=False,
        type=str,
        default=os.path.join(".", "cache_models"),
        help="Directory to cache pre-trained models",
    )

    parser.add_argument(
        "--output",
        required=False,
        type=str,
        default=os.path.join(".", "onnx_models"),
        help="Output directory, or model path ends with .onnx",
    )

    parser.add_argument(
        "-o",
        "--optimize_onnx",
        required=False,
        action="store_true",
        help="Use optimizer.py to optimize onnx model",
    )
    parser.set_defaults(optimize_onnx=False)

    parser.add_argument("--use_gpu", required=False, action="store_true", help="use GPU for inference")
    parser.set_defaults(use_gpu=False)

    parser.add_argument(
        "--provider",
        required=False,
        default=None,
        choices=["dml", "migraphx", "cuda", "tensorrt"],
        help="use dml, cuda, tensorrt or migraphx for respective backend",
    )

    parser.add_argument(
        "--tolerance",
        required=False,
        type=float,
        default=0,
        help="the absolute and relative tolerance for parity verification",
    )

    parser.add_argument(
        "--input_test_file",
        "-i",
        required=False,
        type=str,
        default="",
        help="Path to the file with inputs to test with",
    )

    parser.add_argument(
        "-p",
        "--precision",
        required=False,
        type=Precision,
        default=Precision.FLOAT32,
        choices=list(Precision),
        help="Precision of model to run. fp32 for full precision, fp16 for half or mixed precision, and int8 for quantization",
    )

    parser.add_argument(
        "-t",
        "--test_cases",
        required=False,
        type=int,
        default=1000,
        help="Number of test cases per run for parity",
    )
    parser.add_argument(
        "-r",
        "--test_runs",
        required=False,
        type=int,
        default=10,
        help="Number of runs for parity. It is used for significance test.",
    )

    parser.add_argument("--verbose", required=False, action="store_true")
    parser.set_defaults(verbose=False)

    parser.add_argument("-e", "--use_external_data_format", required=False, action="store_true")
    parser.set_defaults(use_external_data_format=False)

    parser.add_argument("--overwrite", required=False, action="store_true")
    parser.set_defaults(overwrite=False)

    parser.add_argument(
        "--use_int64_inputs",
        required=False,
        action="store_true",
        help="Use int32 instead of int64 for input_ids, position_ids and attention_mask.",
    )
    parser.set_defaults(use_int64_inputs=False)

    parser.add_argument(
        "-s",
        "--stage",
        type=int,
        default=0,
        required=False,
        choices=[0, 1, 2],
        help="Stage in generation: 1 (initial decoder), 2 (decoder), 0 (both). "
        "1 - decode the first token when past_sequence_length is zero; "
        "2 - decode the remaining tokens when past_sequence_length is not zero; "
        "0 - one onnx model for both stages 1 and 2. "
        "Note that we will optimize 1 and 2 differently for best performance.",
    )

    fp16_option_group = parser.add_argument_group(
        'float to float16 conversion parameters that works when "--precision fp16" is specified'
    )

    fp16_option_group.add_argument(
        "-a",
        "--auto_mixed_precision",
        required=False,
        action="store_true",
        help="Convert to mixed precision automatically. Other float16 conversion parameters will be ignored.",
    )
    fp16_option_group.set_defaults(auto_mixed_precision=False)

    fp16_option_group.add_argument(
        "--keep_io_types",
        required=False,
        action="store_true",
        help="Use float32 for past inputs, present and logits outputs.",
    )
    fp16_option_group.set_defaults(keep_io_types=False)

    fp16_option_group.add_argument(
        "--io_block_list",
        nargs="+",
        default=[],
        help="List of inputs or outputs in float32 instead of float16",
    )

    fp16_option_group.add_argument(
        "--op_block_list",
        nargs="+",
        default=[],
        help="List of operators (like Add LayerNormalization SkipLayerNormalization EmbedLayerNormalization FastGelu) "
        "to compute in float32 instead of float16.",
    )

    fp16_option_group.add_argument(
        "--node_block_list",
        nargs="+",
        default=[],
        help="List of node names to compute in float32 instead of float16.",
    )

    fp16_option_group.add_argument(
        "--force_fp16_initializers",
        required=False,
        action="store_true",
        help="Convert all float initializers to float16.",
    )
    fp16_option_group.set_defaults(force_fp16_initializers=False)

    args = parser.parse_args(argv)

    return args


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--model_name_or_path",
        required=True,
        type=str,
        help="Model path, or pretrained model name in the list: " + ", ".join(PRETRAINED_GPT2_MODELS),
    )

    parser.add_argument(
        "--csv",
        required=False,
        type=str,
        default="gpt2_parity_results.csv",
        help="path of csv file to save the result",
    )

    parser.add_argument(
        "--test_cases",
        required=False,
        type=int,
        default=500,
        help="number of test cases per run",
    )

    parser.add_argument("--runs", required=False, type=int, default=40, help="number of repeated runs")

    parser.add_argument("--use_gpu", required=False, action="store_true", help="use GPU for inference")
    parser.set_defaults(use_gpu=False)

    parser.add_argument(
        "--all",
        required=False,
        action="store_true",
        help="run all combinations of mixed precision",
    )
    parser.set_defaults(all=False)

    parser.add_argument("-e", "--use_external_data_format", required=False, action="store_true")
    parser.set_defaults(use_external_data_format=False)

    parser.add_argument("--verbose", required=False, action="store_true")
    parser.set_defaults(verbose=False)

    parser.add_argument(
        "--skip_test",
        required=False,
        action="store_true",
        help="do not run test, and only rank experiments based on existing csv file",
    )
    parser.set_defaults(skip_test=False)

    parser.add_argument(
        "--overwrite",
        required=False,
        action="store_true",
        help="Overwrite existing csv file",
    )
    parser.set_defaults(overwrite=False)

    args = parser.parse_args(argv)

    return args


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--model",
        required=False,
        type=str,
        default="longformer-base-4096",
        help="Checkpoint directory or pre-trained model names in the list: "
        + ", ".join(PRETRAINED_LONGFORMER_MODELS.keys()),
    )

    parser.add_argument(
        "-e",
        "--engine",
        required=False,
        type=str,
        default="onnxruntime",
        choices=["onnxruntime", "torch"],
        help="Engine to benchmark.",
    )

    parser.add_argument(
        "-t",
        "--test_times",
        required=False,
        default=1000,
        type=int,
        help="Number of repeat times to get average inference latency.",
    )

    parser.add_argument("-b", "--batch_sizes", nargs="+", type=int, default=[1])

    # If --export_padding is not used in exporting onnx model, there is no padding in ONNX model,
    # and you will need padding inputs by yourself before running onnx model.
    # Here, we only test sequence length that is multiple of attention window size.
    parser.add_argument(
        "-s",
        "--sequence_lengths",
        nargs="+",
        type=int,
        default=[512, 1024, 2048, 4096],
        help="Sequence lengths. It could have multiple values in latency test."
        "If --export_padding is not used, sequence length shall be multiple of window size.",
    )

    parser.add_argument("--onnx", required=False, type=str, default=None, help="Onnx model path")

    parser.add_argument(
        "-g",
        "--global_lengths",
        nargs="+",
        type=int,
        default=[0],
        help="Number of global tokens. It could have multiple values in latency test.",
    )

    parser.add_argument(
        "-n",
        "--num_threads",
        required=False,
        type=int,
        default=0,
        help="Threads to use.",
    )

    parser.add_argument(
        "--disable_io_binding",
        required=False,
        action="store_true",
        help="Do not use IO Binding.",
    )

    parser.add_argument(
        "--memory",
        required=False,
        action="store_true",
        help="Test memory usage instead of latency.",
    )

    parser.add_argument("--verbose", required=False, action="store_true", help="Print more information.")
    parser.set_defaults(verbose=False)

    parser.add_argument("--use_half4", required=False, action="store_true", help="Use half4 kernel.")
    parser.set_defaults(use_half4=False)

    parser.add_argument("--disable_parity", required=False, action="store_true", help="Do not run parity test.")
    parser.set_defaults(disable_parity=False)

    args = parser.parse_args(argv)

    return args


def parse_arguments():
    """Parse arguments

    Returns:
        args: Namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--model",
        required=False,
        type=str,
        default="longformer-base-4096",
        help="Checkpoint directory or pre-trained model names in the list: "
        + ", ".join(PRETRAINED_LONGFORMER_MODELS.keys()),
    )

    parser.add_argument(
        "--export_padding",
        required=False,
        action="store_true",
        help="Export padding logic to ONNX graph. If not enabled, user need pad input so that sequence length is multiple of window size.",
    )
    parser.set_defaults(export_padding=False)

    parser.add_argument(
        "--no_merge_qkv",
        required=False,
        action="store_true",
        help="Stack the weights of q, k and v on dimension 0 instead of dimension 1.",
    )
    parser.set_defaults(no_merge_qkv=False)

    parser.add_argument(
        "-o",
        "--optimize_onnx",
        required=False,
        action="store_true",
        help="Use optimizer.py to optimize onnx model.",
    )
    parser.set_defaults(optimize_onnx=False)

    parser.add_argument(
        "-p",
        "--precision",
        required=False,
        type=str,
        default="fp32",
        choices=["fp32", "fp16"],
        help="Precision of model to run: fp32 for full precision, fp16 for mixed precision",
    )

    args = parser.parse_args()
    return args


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--model", required=True, type=str, help="bert onnx model path.")

    parser.add_argument(
        "--output_dir",
        required=False,
        type=str,
        default=None,
        help="output test data path. If not specified, .",
    )

    parser.add_argument("--batch_size", required=False, type=int, default=1, help="batch size of input")

    parser.add_argument(
        "--sequence_length",
        required=False,
        type=int,
        default=128,
        help="maximum sequence length of input",
    )

    parser.add_argument(
        "-a",
        "--average_sequence_length",
        default=-1,
        type=int,
        help="average sequence length excluding padding",
    )

    parser.add_argument(
        "-r",
        "--random_sequence_length",
        required=False,
        action="store_true",
        help="use uniform random instead of fixed sequence length",
    )
    parser.set_defaults(random_sequence_length=False)

    parser.add_argument(
        "--global_tokens",
        required=False,
        type=int,
        default=10,
        help="number of global tokens",
    )

    parser.add_argument(
        "--input_ids_name",
        required=False,
        type=str,
        default=None,
        help="input name for input ids",
    )

    parser.add_argument(
        "--input_mask_name",
        required=False,
        type=str,
        default=None,
        help="input name for attention mask",
    )

    parser.add_argument(
        "--global_mask_name",
        required=False,
        type=str,
        default=None,
        help="input name for global attention mask",
    )

    parser.add_argument(
        "--samples",
        required=False,
        type=int,
        default=1,
        help="number of test cases to be generated",
    )

    parser.add_argument("--seed", required=False, type=int, default=3, help="random seed")

    parser.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        help="print verbose information",
    )
    parser.set_defaults(verbose=False)

    args = parser.parse_args()
    return args


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--fp32_cpu",
        required=False,
        action="store_true",
        help="Generate fp32 ONNX model for CPU",
    )

    parser.add_argument(
        "--int4_cpu",
        required=False,
        action="store_true",
        help="Generate int4 ONNX model for CPU",
    )

    parser.add_argument(
        "--fp32_gpu",
        required=False,
        action="store_true",
        help="Generate fp32 ONNX model for Nvidia GPUs",
    )

    parser.add_argument(
        "--fp16_gpu",
        required=False,
        action="store_true",
        help="Generate fp16 ONNX model for Nvidia GPUs",
    )

    parser.add_argument(
        "--int4_gpu",
        required=False,
        action="store_true",
        help="Generate int4 ONNX model for Nvidia GPUs",
    )

    parser.add_argument(
        "--fp16_gpu_sm8x",
        required=False,
        action="store_true",
        help="Generate fp16 ONNX model for Nvidia GPUs with CUDA architecture SM=80~89",
    )

    parser.add_argument(
        "--int4_gpu_sm8x",
        required=False,
        action="store_true",
        help="Generate int4 ONNX model for Nvidia GPUs with CUDA architecture SM=80~89",
    )

    parser.add_argument(
        "--fp16_vllm",
        required=False,
        action="store_true",
        help="Generate fp16 ONNX model for ORT VLLM",
    )

    parser.add_argument(
        "--int4_vllm",
        required=False,
        action="store_true",
        help="Generate int4 ONNX model for ORT VLLM",
    )

    parser.add_argument(
        "--use_cuda_graph",
        required=False,
        action="store_true",
        help="Use CUDA Graph in decoding process",
    )

    parser.add_argument(
        "--overwrite",
        required=False,
        action="store_true",
        help="Overwrite existing ONNX models",
    )

    parser.add_argument(
        "--cache_dir",
        required=False,
        type=str,
        default="./cache",
        help="The cache directory for the pytorch model",
    )

    parser.add_argument(
        "--device_id",
        required=False,
        type=int,
        default=0,
        help="The device id for the pytorch model",
    )

    parser.add_argument(
        "--run_example",
        required=False,
        action="store_true",
        help="Run ORT inference example",
    )

    parser.add_argument(
        "--run_benchmark",
        required=False,
        action="store_true",
        help="Run ORT benchmark",
    )

    parser.add_argument(
        "--skip_export",
        required=False,
        action="store_true",
        help="Skip exporting ONNX model",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        help="The output directory for the ONNX models",
        default="phi2_onnx_models",
    )

    parser.add_argument(
        "--block_size",
        required=False,
        default=16,
        type=int,
        help="Block size to quantize with. See https://github.com/microsoft/onnxruntime/blob/main/onnxruntime/python/tools/quantization/matmul_nbits_quantizer.py for details.",
    )

    parser.add_argument(
        "--int4_accuracy_level",
        required=False,
        type=int,
        help="Accuracy level of the 4-bit quantized MatMul computation. "
        "Refer to the MatMulNBits contrib op's 'accuracy_level' attribute for details "
        "(https://github.com/microsoft/onnxruntime/blob/main/docs/ContribOperators.md#commicrosoftmatmulnbits).",
    )

    args = parser.parse_args()
    return args


def parse_arguments():
    parser = argparse.ArgumentParser(description="Export SAM2 models to ONNX")

    parser.add_argument(
        "--model_type",
        required=False,
        type=str,
        choices=["sam2_hiera_tiny", "sam2_hiera_small", "sam2_hiera_large", "sam2_hiera_base_plus"],
        default="sam2_hiera_large",
        help="The model type to export",
    )

    parser.add_argument(
        "--components",
        required=False,
        nargs="+",
        choices=["image_encoder", "mask_decoder", "prompt_encoder", "image_decoder"],
        default=["image_encoder", "image_decoder"],
        help="Type of ONNX models to export. "
        "Note that image_decoder is a combination of prompt_encoder and mask_decoder",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        help="The output directory for the ONNX models",
        default="sam2_onnx_models",
    )

    parser.add_argument(
        "--dynamic_batch_axes",
        required=False,
        default=False,
        action="store_true",
        help="Export image_encoder with dynamic batch axes",
    )

    parser.add_argument(
        "--multimask_output",
        required=False,
        default=False,
        action="store_true",
        help="Export mask_decoder or image_decoder with multimask_output",
    )

    parser.add_argument(
        "--disable_dynamic_multimask_via_stability",
        required=False,
        action="store_true",
        help="Disable mask_decoder dynamic_multimask_via_stability, and output first mask only."
        "This option will be ignored when multimask_output is True",
    )

    parser.add_argument(
        "--sam2_dir",
        required=False,
        type=str,
        default="./segment-anything-2",
        help="The directory of segment-anything-2 git repository",
    )

    parser.add_argument(
        "--overwrite",
        required=False,
        default=False,
        action="store_true",
        help="Overwrite onnx model file if exists.",
    )

    parser.add_argument(
        "--demo",
        required=False,
        default=False,
        action="store_true",
        help="Run demo with the exported ONNX models.",
    )

    parser.add_argument(
        "--optimize",
        required=False,
        default=False,
        action="store_true",
        help="Optimize onnx models",
    )

    parser.add_argument(
        "--dtype", required=False, choices=["fp32", "fp16"], default="fp32", help="Data type for inference."
    )

    parser.add_argument(
        "--use_gpu",
        required=False,
        default=False,
        action="store_true",
        help="Optimize onnx models for GPU",
    )

    parser.add_argument(
        "--dynamo",
        required=False,
        default=False,
        action="store_true",
        help="Use dynamo for exporting onnx model. Only image_encoder supports dynamo right now.",
    )

    parser.add_argument(
        "--verbose",
        required=False,
        default=False,
        action="store_true",
        help="Print verbose information",
    )

    args = parser.parse_args()
    return args


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-e",
        "--engine",
        required=False,
        type=str,
        default="onnxruntime",
        choices=["onnxruntime", "optimum", "torch", "tensorrt"],
        help="Engines to benchmark. Default is onnxruntime.",
    )

    parser.add_argument(
        "-r",
        "--provider",
        required=False,
        type=str,
        default="cuda",
        choices=list(PROVIDERS.keys()),
        help="Provider to benchmark. Default is CUDAExecutionProvider.",
    )

    parser.add_argument(
        "-t",
        "--tuning",
        action="store_true",
        help="Enable TunableOp and tuning. This will incur longer warmup latency.",
    )

    parser.add_argument(
        "-v",
        "--version",
        required=False,
        type=str,
        choices=list(SD_MODELS.keys()),
        default="1.5",
        help="Stable diffusion version like 1.5, 2.0 or 2.1. Default is 1.5.",
    )

    parser.add_argument(
        "-p",
        "--pipeline",
        required=False,
        type=str,
        default=None,
        help="Directory of saved onnx pipeline. It could be the output directory of optimize_pipeline.py.",
    )

    parser.add_argument(
        "-w",
        "--work_dir",
        required=False,
        type=str,
        default=".",
        help="Root directory to save exported onnx models, built engines etc.",
    )

    parser.add_argument(
        "--enable_safety_checker",
        required=False,
        action="store_true",
        help="Enable safety checker",
    )
    parser.set_defaults(enable_safety_checker=False)

    parser.add_argument(
        "--enable_torch_compile",
        required=False,
        action="store_true",
        help="Enable compile unet for PyTorch 2.0",
    )
    parser.set_defaults(enable_torch_compile=False)

    parser.add_argument(
        "--use_xformers",
        required=False,
        action="store_true",
        help="Use xformers for PyTorch",
    )
    parser.set_defaults(use_xformers=False)

    parser.add_argument(
        "--use_io_binding",
        required=False,
        action="store_true",
        help="Use I/O Binding for Optimum.",
    )
    parser.set_defaults(use_io_binding=False)

    parser.add_argument(
        "--skip_warmup",
        required=False,
        action="store_true",
        help="No warmup.",
    )
    parser.set_defaults(skip_warmup=False)

    parser.add_argument(
        "-b",
        "--batch_size",
        type=int,
        default=1,
        choices=[1, 2, 3, 4, 8, 10, 16, 32],
        help="Number of images per batch. Default is 1.",
    )

    parser.add_argument(
        "--height",
        required=False,
        type=int,
        default=512,
        help="Output image height. Default is 512.",
    )

    parser.add_argument(
        "--width",
        required=False,
        type=int,
        default=512,
        help="Output image width. Default is 512.",
    )

    parser.add_argument(
        "-s",
        "--steps",
        required=False,
        type=int,
        default=50,
        help="Number of steps. Default is 50.",
    )

    parser.add_argument(
        "-n",
        "--num_prompts",
        required=False,
        type=int,
        default=10,
        help="Number of prompts. Default is 10.",
    )

    parser.add_argument(
        "-c",
        "--batch_count",
        required=False,
        type=int,
        choices=range(1, 11),
        default=5,
        help="Number of batches to test. Default is 5.",
    )

    parser.add_argument(
        "-m",
        "--max_trt_batch_size",
        required=False,
        type=int,
        choices=range(1, 16),
        default=4,
        help="Maximum batch size for TensorRT. Change the value may trigger TensorRT engine rebuild. Default is 4.",
    )

    parser.add_argument(
        "-g",
        "--enable_cuda_graph",
        required=False,
        action="store_true",
        help="Enable Cuda Graph. Requires onnxruntime >= 1.16",
    )
    parser.set_defaults(enable_cuda_graph=False)

    args = parser.parse_args()

    return args


def parse_arguments(is_xl: bool, parser):
    engines = ["ORT_CUDA", "ORT_TRT", "TRT", "TORCH"]

    parser.add_argument(
        "-e",
        "--engine",
        type=str,
        default=engines[0],
        choices=engines,
        help="Backend engine in {engines}. "
        "ORT_CUDA is CUDA execution provider; ORT_TRT is Tensorrt execution provider; TRT is TensorRT",
    )

    supported_versions = PipelineInfo.supported_versions(is_xl)
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="xl-1.0" if is_xl else "1.5",
        choices=supported_versions,
        help="Version of Stable Diffusion" + (" XL." if is_xl else "."),
    )

    parser.add_argument(
        "-y",
        "--height",
        type=int,
        default=None,
        help="Height of image to generate (must be multiple of 8).",
    )
    parser.add_argument(
        "-x", "--width", type=int, default=None, help="Height of image to generate (must be multiple of 8)."
    )

    parser.add_argument(
        "-s",
        "--scheduler",
        type=str,
        default=None,
        choices=["DDIM", "EulerA", "UniPC", "LCM"],
        help="Scheduler for diffusion process" + " of base" if is_xl else "",
    )

    parser.add_argument(
        "-wd",
        "--work-dir",
        default=".",
        help="Root Directory to store torch or ONNX models, built engines and output images etc.",
    )

    parser.add_argument(
        "-i",
        "--engine-dir",
        default=None,
        help="Root Directory to store built engines or optimized ONNX models etc.",
    )

    parser.add_argument("prompt", nargs="*", default=[""], help="Text prompt(s) to guide image generation.")

    parser.add_argument(
        "-n",
        "--negative-prompt",
        nargs="*",
        default=[""],
        help="Optional negative prompt(s) to guide the image generation.",
    )
    parser.add_argument(
        "-b",
        "--batch-size",
        type=int,
        default=1,
        choices=[1, 2, 4, 8, 16],
        help="Number of times to repeat the prompt (batch size multiplier).",
    )

    parser.add_argument(
        "-d",
        "--denoising-steps",
        type=int,
        default=None,
        help="Number of denoising steps" + (" in base." if is_xl else "."),
    )

    parser.add_argument(
        "-g",
        "--guidance",
        type=float,
        default=None,
        help="Higher guidance scale encourages to generate images that are closely linked to the text prompt.",
    )

    parser.add_argument(
        "-ls", "--lora-scale", type=float, default=1, help="Scale of LoRA weights, default 1 (must between 0 and 1)"
    )
    parser.add_argument("-lw", "--lora-weights", type=str, default="", help="LoRA weights to apply in the base model")

    if is_xl:
        parser.add_argument(
            "--lcm",
            action="store_true",
            help="Use fine-tuned latent consistency model to replace the UNet in base.",
        )

        parser.add_argument(
            "-rs",
            "--refiner-scheduler",
            type=str,
            default="EulerA",
            choices=["DDIM", "EulerA", "UniPC"],
            help="Scheduler for diffusion process of refiner.",
        )

        parser.add_argument(
            "-rg",
            "--refiner-guidance",
            type=float,
            default=5.0,
            help="Guidance scale used in refiner.",
        )

        parser.add_argument(
            "-rd",
            "--refiner-denoising-steps",
            type=int,
            default=30,
            help="Number of denoising steps in refiner. Note that actual steps is refiner_denoising_steps * strength.",
        )

        parser.add_argument(
            "--strength",
            type=float,
            default=0.3,
            help="A value between 0 and 1. The higher the value less the final image similar to the seed image.",
        )

        parser.add_argument(
            "-r",
            "--enable-refiner",
            action="store_true",
            help="Enable SDXL refiner to refine image from base pipeline.",
        )

    # ONNX export
    parser.add_argument(
        "--onnx-opset",
        type=int,
        default=None,
        choices=range(14, 18),
        help="Select ONNX opset version to target for exported models.",
    )

    # Engine build options.
    parser.add_argument(
        "-db",
        "--build-dynamic-batch",
        action="store_true",
        help="Build TensorRT engines to support dynamic batch size.",
    )
    parser.add_argument(
        "-ds",
        "--build-dynamic-shape",
        action="store_true",
        help="Build TensorRT engines to support dynamic image sizes.",
    )
    parser.add_argument("--max-batch-size", type=int, default=None, choices=[1, 2, 4, 8, 16, 32], help="Max batch size")

    # Inference related options
    parser.add_argument(
        "-nw", "--num-warmup-runs", type=int, default=5, help="Number of warmup runs before benchmarking performance."
    )
    parser.add_argument("--nvtx-profile", action="store_true", help="Enable NVTX markers for performance profiling.")
    parser.add_argument("--seed", type=int, default=None, help="Seed for random generator to get consistent results.")
    parser.add_argument("--deterministic", action="store_true", help="use deterministic algorithms.")
    parser.add_argument("-dc", "--disable-cuda-graph", action="store_true", help="Disable cuda graph.")

    parser.add_argument("--framework-model-dir", default=None, help="framework model directory")

    group = parser.add_argument_group("Options for ORT_CUDA engine only")
    group.add_argument("--enable-vae-slicing", action="store_true", help="True will feed only one image to VAE once.")
    group.add_argument("--max-cuda-graphs", type=int, default=1, help="Max number of cuda graphs to use. Default 1.")
    group.add_argument("--user-compute-stream", action="store_true", help="Use user compute stream.")

    # TensorRT only options
    group = parser.add_argument_group("Options for TensorRT (--engine=TRT) only")
    group.add_argument(
        "--build-all-tactics", action="store_true", help="Build TensorRT engines using all tactic sources."
    )

    args = parser.parse_args()

    set_default_arguments(args)

    # Validate image dimensions
    if args.height % 64 != 0 or args.width % 64 != 0:
        raise ValueError(
            f"Image height and width have to be divisible by 64 but specified as: {args.height} and {args.width}."
        )

    if (args.build_dynamic_batch or args.build_dynamic_shape) and not args.disable_cuda_graph:
        print("[I] CUDA Graph is disabled since dynamic input shape is configured.")
        args.disable_cuda_graph = True

    if args.onnx_opset is None:
        args.onnx_opset = 14 if args.engine == "ORT_CUDA" else 17

    if is_xl:
        if args.version == "xl-turbo":
            if args.lcm:
                print("[I] sdxl-turbo cannot use with LCM.")
                args.lcm = False

        assert args.strength > 0.0 and args.strength < 1.0

        assert not (args.lcm and args.lora_weights), "it is not supported to use both lcm unet and Lora together"

    if args.scheduler == "LCM":
        if args.guidance > 2.0:
            print("[I] Use --guidance=0.0 (no more than 2.0) when LCM scheduler is used.")
            args.guidance = 0.0
        if args.denoising_steps > 16:
            print("[I] Use --denoising_steps=8 (no more than 16) when LCM scheduler is used.")
            args.denoising_steps = 8

    print(args)

    return args


def parse_arguments(argv: list[str] | None = None):
    """Parse arguments

    Returns:
        Namespace: arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=str,
        help="Root of input directory of stable diffusion onnx pipeline with float32 models.",
    )

    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=str,
        help="Root of output directory of stable diffusion onnx pipeline with optimized models.",
    )

    parser.add_argument(
        "--float16",
        required=False,
        action="store_true",
        help="Output models of float16, except some nodes falls back to float32 or bfloat16 to avoid overflow.",
    )
    parser.set_defaults(float16=False)

    parser.add_argument(
        "--bfloat16",
        required=False,
        action="store_true",
        help="Allow bfloat16 as fallback if --float16 is also provided.",
    )
    parser.set_defaults(bfloat16=False)

    parser.add_argument(
        "--force_fp32_ops",
        required=False,
        nargs="+",
        type=str,
        help="Force given operators (like unet:Attention) to run in float32. It is case sensitive!",
    )

    parser.add_argument(
        "--inspect",
        required=False,
        action="store_true",
        help="Save the optimized graph from Onnx Runtime. "
        "This option has no impact on inference performance except it might reduce session creation time.",
    )
    parser.set_defaults(inspect=False)

    parser.add_argument(
        "--overwrite",
        required=False,
        action="store_true",
        help="Overwrite exists files.",
    )
    parser.set_defaults(overwrite=False)

    parser.add_argument(
        "-e",
        "--use_external_data_format",
        required=False,
        action="store_true",
        help="Onnx model larger than 2GB need to use external data format. "
        "If specified, save each onnx model to two files: one for onnx graph, another for weights. "
        "If not specified, use same format as original model by default. ",
    )
    parser.set_defaults(use_external_data_format=None)

    parser.add_argument(
        "--provider",
        required=False,
        type=str,
        default=None,
        help="Execution provider to use.",
    )

    FusionOptions.add_arguments(parser)

    args = parser.parse_args(argv)
    return args


def parse_arguments():
    parser = argparse.ArgumentParser()

    pretrained_models = PRETRAINED_T5_MODELS + PRETRAINED_MT5_MODELS
    parser.add_argument(
        "-m",
        "--model_name_or_path",
        required=False,
        default=PRETRAINED_T5_MODELS[0],
        type=str,
        help="Model path, or pretrained model name in the list: " + ", ".join(pretrained_models),
    )

    parser.add_argument(
        "--model_type",
        required=False,
        type=str,
        default="t5",
        choices=["t5", "mt5"],
        help="Model type: either t5 (default) or mt5",
    )

    parser.add_argument(
        "--cache_dir",
        required=False,
        type=str,
        default=os.path.join(".", "cache_models"),
        help="Directory to cache pre-trained models",
    )

    parser.add_argument(
        "--output",
        required=False,
        type=str,
        default=os.path.join(".", "onnx_models"),
        help="Output directory",
    )

    parser.add_argument(
        "-o",
        "--optimize_onnx",
        required=False,
        action="store_true",
        help="Use optimizer.py to optimize onnx model",
    )
    parser.set_defaults(optimize_onnx=False)

    parser.add_argument("--use_gpu", required=False, action="store_true", help="use GPU for inference")
    parser.set_defaults(use_gpu=False)

    parser.add_argument(
        "-p",
        "--precision",
        required=False,
        type=str,
        default=Precision.FLOAT32.value,
        choices=[Precision.FLOAT32.value, Precision.FLOAT16.value],
        help="Precision of model to run. fp32 for full precision, fp16 for half precision",
    )

    parser.add_argument("--verbose", required=False, action="store_true")
    parser.set_defaults(verbose=False)

    parser.add_argument("-e", "--use_external_data_format", required=False, action="store_true")
    parser.set_defaults(use_external_data_format=False)

    parser.add_argument(
        "-s",
        "--use_decoder_start_token",
        required=False,
        action="store_true",
        help="Use config.decoder_start_token_id. Otherwise, add an extra graph input for decoder_input_ids.",
    )
    parser.set_defaults(use_decoder_start_token=False)

    parser.add_argument(
        "-w",
        "--overwrite",
        required=False,
        action="store_true",
        help="overwrite existing ONNX model",
    )
    parser.set_defaults(overwrite=False)

    parser.add_argument(
        "--disable_auto_mixed_precision",
        required=False,
        action="store_true",
        help="do not use auto mixed precision conversion",
    )
    parser.set_defaults(disable_auto_mixed_precision=False)

    parser.add_argument(
        "--force_fp16_io",
        required=False,
        action="store_true",
        help="Force to convert all float inputs and outputs to fp16 when precision is fp16.",
    )
    parser.set_defaults(force_fp16_io=False)

    parser.add_argument(
        "--use_int64_inputs",
        required=False,
        action="store_true",
        help="Use int64 instead of int32 for input_ids, position_ids and attention_mask.",
    )
    parser.set_defaults(use_int64_inputs=False)

    parser.add_argument(
        "--state_dict_path",
        type=str,
        default="",
        help="filepath to load pre-trained model with custom state dictionary (e.g. pytorch_model.bin)",
    )

    parser.add_argument(
        "--encoder_decoder_init",
        required=False,
        action="store_true",
        help="Combine encoder and decoder kv cache initialization into one model. It is legacy format that will be deprecated.",
    )
    parser.set_defaults(encoder_decoder_init=False)

    args = parser.parse_args()

    return args


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser()

    conversion_args = parser.add_argument_group("Conversion Process Args")
    optional_inputs = parser.add_argument_group("Optional Inputs (for WhisperBeamSearch op)")
    optional_outputs = parser.add_argument_group("Optional Outputs (for WhisperBeamSearch op)")
    quant_args = parser.add_argument_group("INT8 Quantization Args")

    #################################
    # Conversion options for Whisper
    #################################

    conversion_args.add_argument(
        "-m",
        "--model_name_or_path",
        required=False,
        default=PRETRAINED_WHISPER_MODELS[0],
        type=str,
        help="Model path, or pretrained model name in the list: " + ", ".join(PRETRAINED_WHISPER_MODELS),
    )

    conversion_args.add_argument(
        "--model_impl",
        required=False,
        default="hf",
        choices=["hf", "openai"],
        type=str,
        help="Select implementation for export of encoder and decoder subgraphs",
    )

    conversion_args.add_argument(
        "--cache_dir",
        required=False,
        type=str,
        default=os.path.join(".", "cache_models"),
        help="Directory to cache pre-trained models",
    )

    conversion_args.add_argument(
        "--output",
        required=False,
        type=str,
        default=os.path.join(".", "onnx_models"),
        help="Output directory",
    )

    conversion_args.add_argument(
        "-o",
        "--optimize_onnx",
        required=False,
        action="store_true",
        help="Use optimizer.py to optimize onnx model",
    )
    conversion_args.set_defaults(optimize_onnx=False)

    conversion_args.add_argument(
        "--use_gpu",
        required=False,
        action="store_true",
        help="Use GPU for model inference",
    )
    conversion_args.set_defaults(use_gpu=False)

    conversion_args.add_argument(
        "-p",
        "--precision",
        required=False,
        type=Precision,
        default=Precision.FLOAT32,
        choices=[Precision.FLOAT32, Precision.FLOAT16, Precision.INT8, Precision.INT4],
        help="Precision of model to run. fp32 for full precision, fp16 for half precision, int8/int4 for quantization",
    )

    conversion_args.add_argument(
        "--use_int64_inputs",
        required=False,
        action="store_true",
        help="Use int64 instead of int32 for input_ids and attention_mask.",
    )
    conversion_args.set_defaults(use_int64_inputs=False)

    conversion_args.add_argument(
        "-r",
        "--provider",
        required=False,
        type=str,
        default="cpu",
        choices=list(PROVIDERS.keys()),
        help="Provider to benchmark. Default is CPUExecutionProvider.",
    )

    conversion_args.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        help="Enable verbose logging",
    )
    conversion_args.set_defaults(verbose=False)

    conversion_args.add_argument(
        "-e",
        "--use_external_data_format",
        required=False,
        action="store_true",
        help="Save weights in external file. Necessary for 'small', 'medium', and 'large' models. Optional for 'tiny' and 'base' models.",
    )
    conversion_args.set_defaults(use_external_data_format=False)

    conversion_args.add_argument(
        "-w",
        "--overwrite",
        required=False,
        action="store_true",
        help="Overwrite existing ONNX model",
    )
    conversion_args.set_defaults(overwrite=False)

    conversion_args.add_argument(
        "--separate_encoder_and_decoder_init",
        required=False,
        action="store_true",
        help="Do not merge encoder and decoder init to initialize past KV caches. Output 3 instead of 2 ONNX models.",
    )
    conversion_args.set_defaults(separate_encoder_and_decoder_init=False)

    conversion_args.add_argument(
        "--no_beam_search_op",
        required=False,
        action="store_true",
        help="Do not produce model with WhisperBeamSearch op, which chains encdecinit and decoder models into one op.",
    )
    conversion_args.set_defaults(no_beam_search_op=False)

    conversion_args.add_argument(
        "--use_decoder_masked_mha",
        required=False,
        action="store_true",
        help="Use DecoderMaskedMultiHeadAttention kernel for improved performance. This is currently an experimental feature.",
    )
    conversion_args.set_defaults(use_decoder_masked_mha=False)

    #############################################################
    # Optional inputs for Whisper
    # (listed below in the order that WhisperBeamSearch expects)
    #############################################################

    optional_inputs.add_argument(
        "-v",
        "--use_vocab_mask",
        required=False,
        action="store_true",
        help="Use vocab_mask as an extra graph input to enable specific logits processing",
    )
    optional_inputs.set_defaults(use_vocab_mask=False)

    optional_inputs.add_argument(
        "-u",
        "--use_prefix_vocab_mask",
        required=False,
        action="store_true",
        help="Use prefix_vocab_mask as an extra graph input to enable specific logits processing",
    )
    optional_inputs.set_defaults(use_prefix_vocab_mask=False)

    optional_inputs.add_argument(
        "-f",
        "--use_forced_decoder_ids",
        required=False,
        action="store_true",
        help="Use decoder_input_ids as an extra graph input to the beam search op",
    )
    optional_inputs.set_defaults(use_forced_decoder_ids=False)

    optional_inputs.add_argument(
        "-l",
        "--use_logits_processor",
        required=False,
        action="store_true",
        help="Use logits_processor as an extra graph input to enable specific logits processing",
    )
    optional_inputs.set_defaults(use_specific_logits_processor=False)

    optional_inputs.add_argument(
        "--collect_cross_qk",
        required=False,
        action="store_true",
        help="Beam search model collect stacked cross QK.",
    )
    optional_inputs.set_defaults(collect_cross_qk=False)

    optional_inputs.add_argument(
        "--extra_decoding_ids",
        required=False,
        action="store_true",
        help="Need extra starting decoding ids for some feature like cross qk. Default if false.",
    )
    optional_inputs.set_defaults(extra_decoding_ids=False)

    optional_inputs.add_argument(
        "-t",
        "--use_temperature",
        required=False,
        action="store_true",
        help="Use temperature as an extra graph input for the WhisperBeamSearch op",
    )
    optional_inputs.set_defaults(use_temperature=False)

    optional_inputs.add_argument(
        "--no_repeat_ngram_size",
        type=int,
        default=0,
        help="default to 0",
    )

    #############################################################
    # Optional outputs for Whisper
    # (listed below in the order that WhisperBeamSearch expects)
    #############################################################

    optional_outputs.add_argument(
        "--output_sequence_scores",
        required=False,
        action="store_true",
        help="Beam search model output scores for each generated sequence.",
    )
    optional_outputs.set_defaults(output_sequence_scores=False)

    optional_outputs.add_argument(
        "--output_scores",
        required=False,
        action="store_true",
        help="Beam search model output scores over vocab per generated token.",
    )
    optional_outputs.set_defaults(output_scores=False)

    optional_outputs.add_argument(
        "--output_cross_qk",
        required=False,
        action="store_true",
        help="Beam search model output collected qk as output. Also hint collect_cross_qk",
    )
    optional_outputs.set_defaults(output_cross_qk=False)

    optional_outputs.add_argument(
        "--cross_qk_onnx_model",
        required=False,
        type=str,
        default=None,
        help="The model which consumes cross_qk outputs.",
    )

    optional_outputs.add_argument(
        "--output_no_speech_probs",
        required=False,
        action="store_true",
        help="Beam search model output no speech probs which is computed from the encoder/context-decoder graph.",
    )
    optional_outputs.set_defaults(output_no_speech_probs=False)

    ###################################
    # Quantization options for Whisper
    ###################################

    quant_args.add_argument(
        "--accuracy_level",
        default=0,
        required=False,
        type=int,
        help="Accuracy level of the 4-bit quantized MatMul computation.",
    )

    quant_args.add_argument(
        "--quantize_symmetric",
        required=False,
        action="store_true",
        help="Quantize weights symmetrically",
    )
    quant_args.set_defaults(quantize_symmetric=False)

    quant_args.add_argument(
        "--quant_method",
        required=False,
        type=str,
        default="k_quant",
        choices=["k_quant", "k_quant_mixed"],
        help="Quantization method for INT4 precision. "
        "k_quant = k_quant algorithm with all nodes at INT4. "
        "k_quant_mixed = k_quant with mixed precision (sensitive layers at INT8, rest at INT4). "
        "Inspired by llama.cpp k-quant mixed strategy.",
    )

    args = parser.parse_args(argv)

    # Collect cross QKs if either flag is enabled
    args.collect_cross_qk = args.collect_cross_qk or args.output_cross_qk

    # FP32 CPU can be supported here once the DMMHA CPU kernel bugs are fixed
    args.use_decoder_masked_mha = args.use_decoder_masked_mha and args.provider == "cuda"

    return args


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Run Werewolf games with sampled agents.")
    parser.add_argument(
        "-p",
        "--agent_pool_configs",
        type=str,
        nargs="+",
        required=True,
        help="List of paths to YAML files containing agent pools.",
    )
    parser.add_argument(
        "-c",
        "--base_game_config",
        type=str,
        required=True,
        help="Path to the base YAML configuration file for game rules.",
    )
    parser.add_argument(
        "-o", "--output_dir", type=str, default="experiment/sample_game", help="Output directory for logs and replays."
    )
    parser.add_argument("-n", "--num_games", type=int, default=1, help="Number of games to run.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument(
        "-a", "--append_timestamp_to_dir", action="store_true", help="Append a timestamp to the output directory."
    )
    parser.add_argument(
        "-s",
        "--shuffle_player_ids",
        action="store_true",
        help="Shuffle player ids for each game to account for name bias.",
    )
    parser.add_argument(
        "-r", "--use_random_agents", action="store_true", help="Use random agents for all players for fast testing."
    )
    parser.add_argument("--parallel", action="store_true", help="Run games in parallel using multiple processes.")
    parser.add_argument(
        "--without_replacement",
        action="store_true",
        help="If provided, sample agents without replacement. Defaults to sampling with replacement.",
    )
    parser.add_argument(
        "--shuffle_roles",
        action="store_true",
        help="If provided, shuffle the roles from the base config for each game.",
    )
    parser.add_argument("--num_processes", type=int, default=None, help="Number of processes for parallel execution.")
    return parser.parse_args()


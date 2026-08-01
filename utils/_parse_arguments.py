
def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert to packing mode tool for ONNX Runtime. It converts BERT like model to use packing mode."
    )
    parser.add_argument("--input", required=True, type=str, help="input onnx model path")

    parser.add_argument("--output", required=True, type=str, help="optimized onnx model path")

    parser.add_argument("--verbose", required=False, action="store_true", help="show debug information.")
    parser.set_defaults(verbose=False)

    parser.add_argument(
        "--use_external_data_format",
        required=False,
        action="store_true",
        help="use external data format to store large model (>2GB)",
    )
    parser.set_defaults(use_external_data_format=False)

    args = parser.parse_args()

    return args


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Graph optimization tool for ONNX Runtime."
        "It transforms ONNX graph to use optimized operators for Transformer models."
    )
    parser.add_argument("--input", required=True, type=str, help="input onnx model path")

    parser.add_argument("--output", required=True, type=str, help="optimized onnx model path")

    parser.add_argument(
        "--model_type",
        required=False,
        type=str.lower,
        default="bert",
        choices=list(MODEL_TYPES.keys()),
        help="Model type selected in the list: " + ", ".join(MODEL_TYPES.keys()),
    )

    parser.add_argument(
        "--num_heads",
        required=False,
        type=int,
        default=0,
        help="number of attention heads like 12 for bert-base and 16 for bert-large. "
        "Default is 0 to detect automatically for BERT."
        "For other model type, this parameter need specify correctly.",
    )

    parser.add_argument(
        "--hidden_size",
        required=False,
        type=int,
        default=0,
        help="hidden size like 768 for bert-base and 1024 for bert-large. "
        "Default is 0 to detect automatically for BERT. "
        "For other model type, this parameter need specify correctly.",
    )

    parser.add_argument(
        "--input_int32",
        required=False,
        action="store_true",
        help="Use int32 (instead of int64) inputs. "
        "It could avoid unnecessary data cast when EmbedLayerNormalization is fused for BERT.",
    )
    parser.set_defaults(input_int32=False)

    parser.add_argument(
        "--float16",
        required=False,
        action="store_true",
        help="Convert all weights and nodes in float32 to float16. "
        "It has potential loss in precision compared to mixed precision conversion.",
    )
    parser.set_defaults(float16=False)

    FusionOptions.add_arguments(parser)

    parser.add_argument("--verbose", required=False, action="store_true", help="show debug information.")
    parser.set_defaults(verbose=False)

    parser.add_argument(
        "--use_gpu",
        required=False,
        action="store_true",
        help="Use GPU for inference. Set this flag if your model is intended for GPU when opt_level > 1.",
    )
    parser.set_defaults(use_gpu=False)

    parser.add_argument(
        "--provider",
        required=False,
        type=str,
        default=None,
        help="Execution provider to use if use_gpu",
    )

    parser.add_argument(
        "--only_onnxruntime",
        required=False,
        action="store_true",
        help="optimized by onnxruntime only, and no graph fusion in Python",
    )
    parser.set_defaults(only_onnxruntime=False)

    parser.add_argument(
        "--opt_level",
        required=False,
        type=int,
        choices=[0, 1, 2, 3, 99],
        default=None,
        help="onnxruntime optimization level. 0 will disable onnxruntime graph optimization. "
        "The recommended value is 1. When opt_level > 1 is used, optimized model for GPU might not run in CPU. "
        "Level 2, Level 3 and 99 are intended for --only_onnxruntime.",
    )

    parser.add_argument(
        "--use_external_data_format",
        required=False,
        action="store_true",
        help="use external data format to store large model (>2GB)",
    )
    parser.set_defaults(use_external_data_format=False)

    parser.add_argument(
        "--disable_symbolic_shape_infer",
        required=False,
        action="store_true",
        help="disable symbolic shape inference",
    )
    parser.set_defaults(disable_symbolic_shape_infer=False)

    parser.add_argument(
        "--convert_to_packing_mode",
        required=False,
        action="store_true",
        help="convert the model to packing mode. Only available for BERT like model",
    )
    parser.set_defaults(convert_to_packing_mode=False)

    parser.add_argument(
        "--convert_attribute",
        required=False,
        action="store_true",
        help="convert attributes when using a rewritten ONNX model (e.g. Dynamo-exported model from ONNX Script)",
    )
    parser.set_defaults(convert_attribute=False)

    args = parser.parse_args()

    return args


def _parse_arguments():
    parser = argparse.ArgumentParser(description="Benchmark SMA2 for ONNX Runtime and PyTorch.")

    parser.add_argument(
        "--component",
        required=False,
        choices=["image_encoder", "image_decoder"],
        default="image_encoder",
        help="component to benchmark. Choices are image_encoder and image_decoder.",
    )

    parser.add_argument(
        "--dtype", required=False, choices=["fp32", "fp16", "bf16"], default="fp32", help="Data type for inference."
    )

    parser.add_argument(
        "--use_gpu",
        required=False,
        action="store_true",
        help="Use GPU for inference.",
    )
    parser.set_defaults(use_gpu=False)

    parser.add_argument(
        "--use_cuda_graph",
        required=False,
        action="store_true",
        help="Use cuda graph in onnxruntime.",
    )
    parser.set_defaults(use_cuda_graph=False)

    parser.add_argument(
        "--intra_op_num_threads",
        required=False,
        type=int,
        choices=[0, 1, 2, 4, 8, 16],
        default=0,
        help="intra_op_num_threads for onnxruntime. ",
    )

    parser.add_argument(
        "--batch_size",
        required=False,
        type=int,
        default=1,
        help="batch size",
    )

    parser.add_argument(
        "--height",
        required=False,
        type=int,
        default=1024,
        help="image height",
    )

    parser.add_argument(
        "--width",
        required=False,
        type=int,
        default=1024,
        help="image width",
    )

    parser.add_argument(
        "--repeats",
        required=False,
        type=int,
        default=1000,
        help="number of repeats for performance test. Default is 1000.",
    )

    parser.add_argument(
        "--warm_up",
        required=False,
        type=int,
        default=5,
        help="number of runs for warm up. Default is 5.",
    )

    parser.add_argument(
        "--engine",
        required=False,
        type=str,
        default="ort",
        choices=["ort", "torch"],
        help="engine for inference",
    )

    parser.add_argument(
        "--multimask_output",
        required=False,
        default=False,
        action="store_true",
        help="Export mask_decoder or image_decoder with multimask_output",
    )

    parser.add_argument(
        "--prefer_nhwc",
        required=False,
        default=False,
        action="store_true",
        help="Use prefer_nhwc=1 provider option for CUDAExecutionProvider",
    )

    parser.add_argument(
        "--enable_nvtx_profile",
        required=False,
        default=False,
        action="store_true",
        help="Enable nvtx profiling. It will add an extra run for profiling before performance test.",
    )

    parser.add_argument(
        "--enable_ort_profile",
        required=False,
        default=False,
        action="store_true",
        help="Enable ORT profiling.",
    )

    parser.add_argument(
        "--enable_torch_profile",
        required=False,
        default=False,
        action="store_true",
        help="Enable PyTorch profiling. It will add an extra run for profiling before performance test.",
    )

    parser.add_argument(
        "--model_type",
        required=False,
        type=str,
        default="sam2_hiera_large",
        choices=["sam2_hiera_tiny", "sam2_hiera_small", "sam2_hiera_large", "sam2_hiera_base_plus"],
        help="sam2 model name",
    )

    parser.add_argument(
        "--sam2_dir",
        required=False,
        type=str,
        default="./segment-anything-2",
        help="The directory of segment-anything-2 git root directory",
    )

    parser.add_argument(
        "--onnx_path",
        required=False,
        type=str,
        default="./sam2_onnx_models/sam2_hiera_large_image_encoder.onnx",
        help="path of onnx model",
    )

    parser.add_argument(
        "--torch_compile_mode",
        required=False,
        type=str,
        default=None,
        choices=["reduce-overhead", "max-autotune", "max-autotune-no-cudagraphs", "none"],
        help="torch compile mode. none will disable torch compile.",
    )

    args = parser.parse_args()

    return args


def _parse_arguments():
    """Parse cmdline arguments."""
    parser = argparse.ArgumentParser(description="Arguments for QNN model preprocess.")

    parser.add_argument("--input_model_path", "-i", required=True, help="Path to the input ONNX model.")
    parser.add_argument("--output_model_path", "-o", required=True, help="Path to the output ONNX model.")

    # Save preprocessed model with external data.
    parser.add_argument(
        "--save_as_external_data",
        action="store_true",
        help="Whether the output model would be saved with external data.",
    )
    parser.add_argument(
        "--all_tensors_to_one_file",
        action="store_true",
        help="Whether to save all external data in one file or save each tensor to a file named with the tensor name.",
    )
    parser.add_argument(
        "--external_data_location",
        help="Filename of the external file where all tensors are saved. The path is relative to the model path.",
    )
    parser.add_argument(
        "--external_data_size_threshold",
        default=1024,
        type=int,
        help="Tensors with data size larger than this threshold are converted to external data.",
    )
    parser.add_argument(
        "--external_data_convert_attribute",
        action="store_true",
        help="Whether to save all tensors, including attribute tensors, to external data.",
    )

    # Preprocess options.
    parser.add_argument(
        "--fuse_layernorm",
        action="store_true",
        help="Whether to fuse matched sequences into LayerNormalization nodes if possible.",
    )

    # I/O layouts.
    parser.add_argument(
        "--inputs_to_make_channel_last",
        nargs="+",
        default=None,
        help="List of graph input names to be transposed into channel-last.",
    )

    parser.add_argument(
        "--outputs_to_make_channel_last",
        nargs="+",
        default=None,
        help="List of graph output names to be transposed into channel-last.",
    )

    # Fix dynamic input shapes.
    parser.add_argument(
        "--dynamic_input_shapes",
        nargs=2,
        action="append",
        type=str,
        default=None,
        help="Model input name and desired static shape in comma seprated format, for example: 'input' 1,3,256,256",
    )

    # Exclude initializer from input
    parser.add_argument(
        "--exclude_initializer_from_input",
        action="store_true",
        help="Whether to exclude initializer from input if model.ir_version >= 4",
    )

    return parser.parse_args()



def user_command():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--max_length", type=int, default=20, help="default to 20")
    parent_parser.add_argument("--min_length", type=int, default=0, help="default to 0")
    parent_parser.add_argument("-o", "--output", type=str, default="onnx_models", help="default name is onnx_models.")
    parent_parser.add_argument("-i", "--input_text", type=str, default=None, help="input text")
    parent_parser.add_argument("-s", "--spm_path", type=str, default=None, help="tokenizer model from sentencepice")
    parent_parser.add_argument("-v", "--vocab_path", type=str, help="vocab dictionary")
    parent_parser.add_argument("-b", "--num_beams", type=int, default=5, help="default to 5")
    parent_parser.add_argument("--repetition_penalty", type=float, default=1.0, help="default to 1.0")
    parent_parser.add_argument("--no_repeat_ngram_size", type=int, default=3, help="default to 3")
    parent_parser.add_argument("--early_stopping", type=bool, default=False, help="default to False")
    parent_parser.add_argument("--opset_version", type=int, default=14, help="minimum is 14")

    parent_parser.add_argument("--no_encoder", action="store_true")
    parent_parser.add_argument("--no_decoder", action="store_true")
    parent_parser.add_argument("--no_chain", action="store_true")
    parent_parser.add_argument("--no_inference", action="store_true")

    required_args = parent_parser.add_argument_group("required input arguments")
    required_args.add_argument(
        "-m",
        "--model_dir",
        type=str,
        required=True,
        help="The directory contains input huggingface model. \
                               An official model like facebook/bart-base is also acceptable.",
    )

    print_args(parent_parser.parse_args())
    return parent_parser.parse_args()


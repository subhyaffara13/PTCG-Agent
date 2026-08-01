
def get_ort_model_inputs_len(args, model):
    if args.benchmark_type in {"hf-pt-eager", "hf-pt-compile"}:
        return 0
    if args.benchmark_type == "hf-ort":
        try:
            # New Optimum export (https://github.com/huggingface/optimum/blob/888332364c2e0091da1fc974737c7e277af168bf/optimum/onnxruntime/modeling_ort.py#L268)
            return len(model.inputs_names)
        except Exception:
            # Old Optimum export (https://github.com/huggingface/optimum/blob/c5ad7f971cb0a494eac03dc0909f146725f999c5/optimum/onnxruntime/base.py#L54)
            return len(model.decoder.input_names)
    return len(model.get_inputs())


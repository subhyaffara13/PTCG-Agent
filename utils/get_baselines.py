
def get_baselines(args):
    model = args.model_name_or_path
    fp32_baseline = f"-m {model} -o -p fp32".split()
    if args.use_gpu:
        fp32_baseline.append("--use_gpu")
    if args.use_external_data_format:
        fp32_baseline.append("--use_external_data_format")

    fp16_baseline = f"-m {model} -o --use_gpu -p fp16".split()
    if args.use_external_data_format:
        fp16_baseline.append("--use_external_data_format")

    return fp32_baseline, fp16_baseline


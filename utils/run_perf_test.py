
def run_perf_test(args):
    features = "gpu" if args.use_gpu else "cpu"
    csv_filename = "benchmark_sam_{}_{}_{}.csv".format(
        features,
        args.engine,
        datetime.now().strftime("%Y%m%d-%H%M%S"),
    )
    with open(csv_filename, mode="a", newline="") as csv_file:
        column_names = [
            "model_type",
            "component",
            "dtype",
            "use_gpu",
            "enable_cuda_graph",
            "prefer_nhwc",
            "use_tf32",
            "batch_size",
            "height",
            "width",
            "multi_mask_output",
            "num_labels",
            "num_points",
            "num_masks",
            "intra_op_num_threads",
            "warm_up",
            "repeats",
            "enable_nvtx_profile",
            "torch_compile_mode",
            "engine",
            "average_latency",
        ]
        csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
        csv_writer.writeheader()

        run_test(args, csv_writer)


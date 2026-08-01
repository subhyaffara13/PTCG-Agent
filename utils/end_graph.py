
def end_graph(output_file):
    if len(collected_calls) == 0:
        return
    overall_time = sum(call[0] for call in collected_calls)
    overall_gb = sum(call[1] for call in collected_calls)
    cur_file = inspect.stack()[1].filename
    summary_str = (
        f"SUMMARY ({cur_file})\n"
        f"{overall_time:.2f}ms   \t {overall_gb:.2f} GB\t {overall_gb / (overall_time / 1e3):.2f}GB/s"
    )
    log.info(
        "%s",
        summary_str,
    )
    if output_file is not None:
        # sort perf numbers in descending order, i.e. placing the
        # most runtime-heavy kernels at the top of the list
        sorted_calls = sorted(collected_calls, key=lambda c: float(c[0]), reverse=True)
        try:
            with open(output_file, "a") as file:
                log.info(
                    "Save profile bandwidth results to %s",
                    output_file,
                )
                file.write("====================\n")
                file.write(f"TRITON KERNELS BANDWIDTH INFO ({cur_file})\n")
                for ms, num_gb, gb_per_s, kernel_name in sorted_calls:
                    # also display the runtime percentage for each kernel
                    percentage = f"{ms / overall_time * 100:.2f}%"
                    suffix = f" \t {percentage} \t {kernel_name}"
                    bw_info_str = create_bandwidth_info_str(
                        ms,
                        num_gb,
                        gb_per_s,
                        suffix=suffix,
                        color=False,
                    )
                    file.write(bw_info_str + "\n")
                file.write(f"{summary_str}\n\n")
        except Exception:
            log.warning(
                "failed to write profile bandwidth result into %s",
                output_file,
                exc_info=True,
            )


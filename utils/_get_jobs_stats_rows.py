from typing import Any

def _get_jobs_stats_rows(
    job_id: str, metrics_stream: Iterable[dict[str, Any]], table_headers: list[str]
) -> Iterable[tuple[bool, str, list[list[str | int]]]]:
    for metrics in metrics_stream:
        row = [
            job_id,
            f"{metrics['cpu_usage_pct']}%",
            round(metrics["cpu_millicores"] / 1000.0, 1),
            f"{round(100 * metrics['memory_used_bytes'] / metrics['memory_total_bytes'], 2)}%",
            f"{_format_size(metrics['memory_used_bytes'])}B / {_format_size(metrics['memory_total_bytes'])}B",
            f"{_format_size(metrics['rx_bps'])}bps / {_format_size(metrics['tx_bps'])}bps",
        ]
        if metrics["gpus"] and isinstance(metrics["gpus"], dict):
            rows = [row] + [[""] * len(row)] * (len(metrics["gpus"]) - 1)
            for row, gpu_id in zip(rows, sorted(metrics["gpus"])):
                gpu = metrics["gpus"][gpu_id]
                row += [
                    f"{gpu['utilization']}%",
                    f"{round(100 * gpu['memory_used_bytes'] / gpu['memory_total_bytes'], 2)}%",
                    f"{_format_size(gpu['memory_used_bytes'])}B / {_format_size(gpu['memory_total_bytes'])}B",
                ]
        else:
            row += ["N/A"] * (len(table_headers) - len(row))
            rows = [row]
        yield False, job_id, rows
    yield True, job_id, []


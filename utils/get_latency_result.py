
def get_latency_result(latency_list, batch_size):
    latency_ms = sum(latency_list) / float(len(latency_list)) * 1000.0
    latency_variance = numpy.var(latency_list, dtype=numpy.float64) * 1000.0
    throughput = batch_size * (1000.0 / latency_ms)

    return {
        "test_times": len(latency_list),
        "latency_variance": f"{latency_variance:.2f}",
        "latency_90_percentile": f"{numpy.percentile(latency_list, 90) * 1000.0:.2f}",
        "latency_95_percentile": f"{numpy.percentile(latency_list, 95) * 1000.0:.2f}",
        "latency_99_percentile": f"{numpy.percentile(latency_list, 99) * 1000.0:.2f}",
        "average_latency_ms": f"{latency_ms:.2f}",
        "QPS": f"{throughput:.2f}",
    }


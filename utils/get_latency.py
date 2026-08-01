
def get_latency(row):
    for name in row:
        if name.startswith("average_latency(batch_size="):
            return float(row[name])

    raise RuntimeError("Failed to get average_latency from output")


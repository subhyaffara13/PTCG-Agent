import json

def process_log_file(device_id, log_file, base_results):
    entries = []
    batch_size, sequence_length, step = None, None, None
    latency_s, latency_ms, throughput, memory = None, None, None, None

    batch_pattern = "Batch Size: "
    sequence_pattern = "Sequence Length: "
    prompt_step_pattern = "to get past_key_values"
    per_token_step_pattern = "with past_key_values"
    latency_pattern = "Latency: "
    throughput_pattern = "Throughput: "
    memory_pattern = "peak="

    with open(log_file) as f:
        for input_line in f:
            line = input_line.replace("\n", "")

            if batch_pattern in line:
                batch_size = int(line[len(batch_pattern) :])
            elif sequence_pattern in line:
                sequence_length = int(line[len(sequence_pattern) :])
            elif prompt_step_pattern in line:
                step = "prompt"
            elif per_token_step_pattern in line:
                step = "per-token"
            elif latency_pattern in line:
                latency_s = float(line[len(latency_pattern) : line.rfind(" ")])
                latency_ms = latency_s * 1000
            elif throughput_pattern in line:
                throughput = float(line[len(throughput_pattern) : line.rfind(" ")])
            elif memory_pattern in line:
                if "CPU" in line:
                    # Example format for log entry:
                    # CPU memory usage: before=1000.0 MB, peak=2000.0 MB
                    memory = float(line[line.rfind("=") + 1 : line.rfind(" MB")]) / 1000
                else:
                    # Example format for log entry:
                    # GPU memory usage: before=[{'device_id': 0, 'name': 'NVIDIA A100-SXM4-80GB', 'max_used_MB': 69637.25}, {'device_id': 1, 'name': 'NVIDIA A100-SXM4-80GB', 'max_used_MB': 890.625}]  peak=[{'device_id': 0, 'name': 'NVIDIA A100-SXM4-80GB', 'max_used_MB': 73861.25}, {'device_id': 1, 'name': 'NVIDIA A100-SXM4-80GB', 'max_used_MB': 890.625}]
                    peak = line[line.find(memory_pattern) + len(memory_pattern) :].replace("'", '"')
                    usage = json.loads(peak)[device_id]["max_used_MB"]
                    memory = float(usage) / 1000

                # Append log entry to list of entries
                entry = base_results + [  # noqa: RUF005
                    batch_size,
                    sequence_length,
                    step,
                    latency_s,
                    latency_ms,
                    throughput,
                    memory,
                ]
                entries.append(entry)

    return entries


def process_log_file(device_id, log_file, base_results):
    entries = []

    # Detect steps in speech pipeline
    step = None
    load_audio_pattern = "Load audio: "
    feat_ext_pattern = "Feature extraction: "
    pytorch_pattern = "Evaluating PyTorch..."
    onnxruntime_pattern = "Evaluating ONNX Runtime..."

    load_audio_latency_s, load_audio_throughput_s = None, None
    feat_ext_latency_s, feat_ext_throughput_s = None, None
    token_length, latency_s, per_token_latency_s, per_token_latency_ms = None, None, None, None
    throughput, memory = None, None

    # Detect metrics
    latency_pattern = "Latency: "
    throughput_pattern = "Throughput: "
    token_length_pattern = "Generated token length: "
    memory_pattern = "peak="

    with open(log_file) as f:
        for input_line in f:
            line = input_line.replace("\n", "")

            # Get step in speech recognition pipeline
            if load_audio_pattern in line:
                step = "load-audio"
            elif feat_ext_pattern in line:
                step = "feature-extraction"
            elif pytorch_pattern in line or onnxruntime_pattern in line:
                step = "process"

            # Check metrics
            if latency_pattern in line:
                latency_s = float(line[len(latency_pattern) : line.rfind(" ")])
            elif throughput_pattern in line:
                throughput = float(line[len(throughput_pattern) : line.rfind(" ")])
                if step == "load-audio":
                    load_audio_latency_s, load_audio_throughput_s = latency_s, throughput
                    step = None
                if step == "feature-extraction":
                    feat_ext_latency_s, feat_ext_throughput_s = latency_s, throughput
                    step = None
            elif token_length_pattern in line:
                token_length = int(line[len(token_length_pattern) : line.rfind(" ")])
                per_token_latency_s = latency_s / token_length
                per_token_latency_ms = per_token_latency_s * 1000
            elif memory_pattern in line:
                if "CPU" in line:
                    # Example format for log entry:
                    # CPU memory usage: before=1000.0 MB, peak=2000.0 MB
                    memory = float(line[line.rfind("=") + 1 : line.rfind(" MB")]) / 1000
                else:
                    # Example format for log entry:
                    # GPU memory usage: before=[{'device_id': 0, 'name': 'Tesla V100-PCIE-16GB', 'max_used_MB': 1638.875}, {'device_id': 1, 'name': 'Tesla V100-PCIE-16GB', 'max_used_MB': 236.875},  peak=[{'device_id': 0, 'name': 'Tesla V100-PCIE-16GB', 'max_used_MB': 1780.875}, {'device_id': 1, 'name': 'Tesla V100-PCIE-16GB', 'max_used_MB': 236.875}]
                    peak = line[line.find(memory_pattern) + len(memory_pattern) :].replace("'", '"')
                    usage = json.loads(peak)[device_id]["max_used_MB"]
                    memory = float(usage) / 1000

                # Calculate real-time factor (RTF):
                # RTF = total latency / audio duration
                total_latency = (
                    (load_audio_latency_s if load_audio_latency_s else 0)
                    + (feat_ext_latency_s if feat_ext_latency_s else 0)
                    + (latency_s if latency_s else 0)
                )
                audio_duration = base_results[-1]
                rtf = (total_latency / audio_duration) if audio_duration else -1
                logger.info(f"Total latency: {total_latency} s")
                logger.info(f"Audio duration: {audio_duration} s")
                logger.info(f"Real-time factor: {rtf}")

                # Append log entry to list of entries
                entry = base_results + [  # noqa: RUF005
                    token_length,
                    load_audio_latency_s,
                    load_audio_throughput_s,
                    feat_ext_latency_s if feat_ext_latency_s else -1,
                    feat_ext_throughput_s if feat_ext_throughput_s else -1,
                    latency_s,
                    per_token_latency_ms,
                    throughput,
                    memory,
                    rtf,
                ]
                entries.append(entry)

    return entries


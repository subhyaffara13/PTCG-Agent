
def add_to_mapping(layer_name, device, repo_name, mode, compatible_mapping):
    from kernels import LayerRepository

    if device not in ["cuda", "rocm", "xpu", "npu", "neuron", "tpu"]:
        raise ValueError(f"Only cuda, rocm, xpu, npu, neuron and tpu devices supported, got: {device}")
    repo_layer_name = repo_name.split(":")[1]
    repo_id = repo_name.split(":")[0]
    compatible_mapping[layer_name] = {
        device: {
            mode: LayerRepository(
                repo_id=repo_id,
                layer_name=repo_layer_name,
            )
        }
    }


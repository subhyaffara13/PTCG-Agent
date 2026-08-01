
def add_to_mapping_local(layer_name, device, repo_name, mode, compatible_mapping):
    from pathlib import Path

    from kernels import LocalLayerRepository

    if device not in ["cuda", "rocm", "xpu", "npu", "neuron", "tpu"]:
        raise ValueError(f"Only cuda, rocm, xpu, npu, neuron and tpu devices supported, got: {device}")
    repo_layer_name = repo_name.split(":")[1]
    repo_path = repo_name.split(":")[0]
    repo_package_name = repo_path.split("/")[-1]
    compatible_mapping[layer_name] = {
        device: {
            mode: LocalLayerRepository(
                repo_path=Path(repo_path),
                package_name=repo_package_name,
                layer_name=repo_layer_name,
            )
        }
    }


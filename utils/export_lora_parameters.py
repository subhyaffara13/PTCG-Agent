
def export_lora_parameters(
    npz_file_path: os.PathLike, adapter_version: int, model_version: int, output_file_path: os.PathLike
):
    """The function converts lora parameters in npz to onnx_adapter format"""
    adapter_format = ort.AdapterFormat()
    adapter_format.set_adapter_version(adapter_version)
    adapter_format.set_model_version(model_version)
    name_to_ort_value = {}
    with np.load(npz_file_path) as data:
        for name, np_arr in data.items():
            ort_value = ort.OrtValue.ortvalue_from_numpy(np_arr)
            name_to_ort_value[name] = ort_value

    adapter_format.set_parameters(name_to_ort_value)
    adapter_format.export_adapter(output_file_path)


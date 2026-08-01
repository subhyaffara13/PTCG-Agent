
def get_max_num_sms() -> int:
    if torch.xpu.is_available():
        return torch.xpu.get_device_properties().gpu_subslice_count
    return torch.cuda.get_device_properties("cuda").multi_processor_count


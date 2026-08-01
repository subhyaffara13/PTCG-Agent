
def get_intel_gpu_detected(run_lambda):
    if not TORCH_AVAILABLE or not hasattr(torch, "xpu"):
        return "N/A"

    device_count = torch.xpu.device_count()
    if device_count == 0:
        return "N/A"

    devices = [
        f"* [{i}] {torch.xpu.get_device_properties(i)}" for i in range(device_count)
    ]
    return "\n".join(devices)


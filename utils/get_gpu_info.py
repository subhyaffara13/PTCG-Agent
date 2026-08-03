import re
from typing import Any

def get_gpu_info(run_lambda):
    if get_platform() == "darwin" or (
        TORCH_AVAILABLE
        and hasattr(torch.version, "hip")
        and torch.version.hip is not None
    ):
        if TORCH_AVAILABLE and torch.cuda.is_available():
            if torch.version.hip is not None:
                prop = torch.cuda.get_device_properties(0)
                if hasattr(prop, "gcnArchName"):
                    gcnArch = " ({})".format(prop.gcnArchName)
                else:
                    gcnArch = "NoGCNArchNameOnOldPyTorch"
            else:
                gcnArch = ""
            return torch.cuda.get_device_name(None) + gcnArch
        return None
    smi = get_nvidia_smi()
    uuid_regex = re.compile(r" \(UUID: .+?\)")
    rc, out, _ = run_lambda(smi + " -L")
    if rc != 0:
        return None
    # Anonymize GPUs by removing their UUID
    return re.sub(uuid_regex, "", out)


def get_gpu_info() -> list[dict[str, Any]] | None:
    from py3nvml.py3nvml import (  # noqa: PLC0415
        NVMLError,
        nvmlDeviceGetCount,
        nvmlDeviceGetHandleByIndex,
        nvmlDeviceGetMemoryInfo,
        nvmlDeviceGetName,
        nvmlInit,
        nvmlShutdown,
    )

    try:
        nvmlInit()
        result = []
        device_count = nvmlDeviceGetCount()
        if not isinstance(device_count, int):
            return None

        for i in range(device_count):
            info = nvmlDeviceGetMemoryInfo(nvmlDeviceGetHandleByIndex(i))
            if isinstance(info, str):
                return None
            result.append(
                {
                    "id": i,
                    "name": nvmlDeviceGetName(nvmlDeviceGetHandleByIndex(i)),
                    "total": info.total,
                    "free": info.free,
                    "used": info.used,
                }
            )
        nvmlShutdown()
        return result
    except NVMLError as error:
        print("Error fetching GPU information using nvml: %s", error)
        return None


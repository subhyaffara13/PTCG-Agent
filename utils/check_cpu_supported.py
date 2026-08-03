import os
import sys

def check_cpu_supported():
    requires_avx2_on_cpu = (
        torch.cpu._is_avx2_supported() and os.getenv("ATEN_CPU_CAPABILITY") != "default"
    )
    supported = (
        requires_avx2_on_cpu
        and not torch.xpu.is_available()
        and sys.platform != "darwin"
    )
    return supported


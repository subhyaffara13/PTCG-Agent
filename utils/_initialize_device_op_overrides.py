
def _initialize_device_op_overrides():
    # Use a flag rather than checking device_op_overrides_dict, since external/test
    # code may partially populate it before we are called.
    global _device_op_overrides_initialized
    if _device_op_overrides_initialized:
        return

    from . import mps_device_op_overrides  # noqa: F401
    from .cpu_device_op_overrides import CpuDeviceOpOverrides
    from .cuda import device_op_overrides  # noqa: F401
    from .mtia import device_op_overrides as mtia_op_overrides  # noqa: F401
    from .xpu import device_op_overrides as xpu_op_overrides  # noqa: F401

    # TPU uses Pallas for codegen and only needs no-op overrides
    register_device_op_overrides("tpu", CpuDeviceOpOverrides())

    _device_op_overrides_initialized = True


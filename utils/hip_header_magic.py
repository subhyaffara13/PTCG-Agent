
def hip_header_magic(input_string):
    """If the file makes kernel builtin calls and does not include the cuda_runtime.h header,
    then automatically add an #include to match the "magic" includes provided by NVCC.
    TODO:
        Update logic to ignore cases where the cuda_runtime.h is included by another file.
    """

    # Copy the input.
    output_string = input_string

    # Check if one of the following headers is already included.
    headers = ["hip/hip_runtime.h", "hip/hip_runtime_api.h"]
    if any(re.search(fr'#include ("{ext}"|<{ext}>)', output_string) for ext in headers):
        return output_string

    # Rough logic to detect if we're inside device code
    hasDeviceLogic: int
    hasDeviceLogic = "hipLaunchKernelGGL" in output_string
    hasDeviceLogic += "__global__" in output_string
    hasDeviceLogic += "__shared__" in output_string
    hasDeviceLogic += RE_SYNCTHREADS.search(output_string) is not None

    # If device logic found, provide the necessary header.
    if hasDeviceLogic:
        output_string = '#include "hip/hip_runtime.h"\n' + input_string

    return output_string


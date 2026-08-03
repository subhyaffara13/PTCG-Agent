import math


def spec_to_bytes(spec: "dtensor_spec.DTensorSpec") -> int:
    if spec.tensor_meta is None:
        raise AssertionError("spec should have tensor meta defined!")
    return spec.tensor_meta.dtype.itemsize * math.prod(spec.shape)


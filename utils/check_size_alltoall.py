from typing import Any
import math


def check_size_alltoall(alltoall_cases: list[dict[str, Any]]) -> tuple[bool, int, int]:
    input_numel = 0
    output_numel = 0
    for e in alltoall_cases:
        input_numel += math.prod(e["input_sizes"][0])
        output_numel += math.prod(e["output_sizes"][0])
    return input_numel != output_numel, input_numel, output_numel


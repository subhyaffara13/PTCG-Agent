import copy
from typing import Callable

def get_default_float_to_quantized_operator_mappings() -> dict[
    Callable | str, Callable
]:
    return copy.deepcopy(DEFAULT_FLOAT_TO_QUANTIZED_OPERATOR_MAPPINGS)


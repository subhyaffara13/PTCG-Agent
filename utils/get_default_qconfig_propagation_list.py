import copy
from typing import Callable

def get_default_qconfig_propagation_list() -> set[Callable]:
    """Get the default list of module types that we'll attach qconfig
    attribute to in prepare
    """
    QCONFIG_PROPAGATE_MODULE_CLASS_LIST = (
        set(DEFAULT_STATIC_QUANT_MODULE_MAPPINGS.keys())
        | set(DEFAULT_QAT_MODULE_MAPPINGS.keys())
        | set(DEFAULT_DYNAMIC_QUANT_MODULE_MAPPINGS.keys())
        | _INCLUDE_QCONFIG_PROPAGATE_LIST
    )
    return copy.deepcopy(QCONFIG_PROPAGATE_MODULE_CLASS_LIST)


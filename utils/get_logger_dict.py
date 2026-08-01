
def get_logger_dict(mod: nn.Module, prefix: str = "") -> dict[str, dict]:
    r"""Traverse the modules and save all logger stats into target dict.
    This is mainly used for quantization accuracy debug.

    Type of loggers supported:
        ShadowLogger: used to log the outputs of the quantized module and its matching float shadow module,
        OutputLogger: used to log the outputs of the modules

    Args:
        mod: module we want to save all logger stats
        prefix: prefix for the current module

    Return:
        target_dict: the dictionary used to save all logger stats

    """
    torch._C._log_api_usage_once("quantization_api._numeric_suite.get_logger_dict")

    target_dict: dict[str, dict] = {}
    _get_logger_dict_helper(mod, target_dict, prefix)
    return target_dict



def gen_has_torch_function_check(
    name: BaseOperatorName, module: str | None, *, noarg: bool, method: bool
) -> str:
    if noarg:
        if method:
            return f"""\
if(check_has_torch_function(self_)) {{
  return handle_torch_function(self_, "{name}");
}}
"""
        else:
            return ""

    self_ = "self_" if method else "nullptr"
    namespace = (
        {
            "torch": "THPVariableFunctionsModule",
            "torch.nn": "THPNNVariableFunctionsModule",
            "torch.fft": "THPFFTVariableFunctionsModule",
            "torch.linalg": "THPLinalgVariableFunctionsModule",
            "torch.nested": "THPNestedVariableFunctionsModule",
            "torch.sparse": "THPSparseVariableFunctionsModule",
            "torch.special": "THPSpecialVariableFunctionsModule",
        }[module]
        if module
        else "THPVariableClass"
    )

    return f"""\
if(_r.has_torch_function()) {{
  return handle_torch_function(_r, {self_}, args, kwargs, {namespace}, "{module or "torch.Tensor"}");
}}
"""


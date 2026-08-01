
def _declare_state(vartype: str, varname: str, initial_value: _T) -> _T:
    _state_vars[varname] = vartype
    return initial_value


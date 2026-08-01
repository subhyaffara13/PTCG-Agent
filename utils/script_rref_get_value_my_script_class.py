
def script_rref_get_value_my_script_class(rref: RRef[MyScriptClass]) -> int:
    return rref.to_here().get_value()


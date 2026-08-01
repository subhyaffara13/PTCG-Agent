
def test_no_globals():

    # Replicate creating the default global_dict:
    default_globals = {}
    exec('from sympy import *', default_globals)
    builtins_dict = vars(builtins)
    for name, obj in builtins_dict.items():
        if isinstance(obj, types.BuiltinFunctionType):
            default_globals[name] = obj
    default_globals['max'] = Max
    default_globals['min'] = Min

    # Need to include Symbol or parse_expr will not work:
    default_globals.pop('Symbol')
    global_dict = {'Symbol':Symbol}

    for name in default_globals:
        obj = parse_expr(name, global_dict=global_dict)
        assert obj == Symbol(name)



def get_param(
    program: "ExportedProgram",
    node: torch.fx.Node,
) -> torch.nn.Parameter | None:
    """
    Returns the parameter associated with the given node in the exported program.
    Returns None if the node is not a parameter within the exported program
    """

    if is_param(program, node):
        parameter_name = program.graph_signature.inputs_to_parameters[node.name]
        return program.state_dict[parameter_name]

    return None


def get_param(module, attr):
    """Get the parameter given a module and attribute.

    Sometimes the weights/bias attribute gives you the raw tensor, but sometimes
    gives a function that will give you the raw tensor, this function takes care of that logic
    """
    param = getattr(module, attr, None)
    if callable(param):
        return param()
    else:
        return param


def get_param(param_name, params):
  return params.get(param_name, _DEFAULT_PARAMS[param_name])


def get_param(param_name, params):
  return params.get(param_name, _DEFAULT_PARAMS[param_name])


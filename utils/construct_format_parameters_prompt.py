
def construct_format_parameters_prompt(parameters: dict):
    parameter_str = "<parameter>\n"
    for k, v in parameters.items():
        parameter_str += f"<{k}>"
        parameter_str += f"{v}"
        parameter_str += f"</{k}>"
    parameter_str += "\n</parameter>"
    return parameter_str


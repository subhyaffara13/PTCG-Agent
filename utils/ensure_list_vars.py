
def ensure_list_vars(arg_vars, variable: str, columns) -> list:
    if arg_vars is not None:
        if not is_list_like(arg_vars):
            return [arg_vars]
        elif isinstance(columns, MultiIndex) and not isinstance(arg_vars, list):
            raise ValueError(
                f"{variable} must be a list of tuples when columns are a MultiIndex"
            )
        else:
            return list(arg_vars)
    else:
        return []


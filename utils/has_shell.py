
def has_shell(context):
    keywords = context.node.keywords
    result = False
    if "shell" in context.call_keywords:
        for key in keywords:
            if key.arg == "shell":
                val = key.value
                if isinstance(val, ast.Constant) and (
                    isinstance(val.value, int)
                    or isinstance(val.value, float)
                    or isinstance(val.value, complex)
                ):
                    result = bool(val.value)
                elif isinstance(val, ast.List):
                    result = bool(val.elts)
                elif isinstance(val, ast.Dict):
                    result = bool(val.keys)
                elif isinstance(val, ast.Name) and val.id in ["False", "None"]:
                    result = False
                elif isinstance(val, ast.Constant):
                    result = val.value
                else:
                    result = True
    return result


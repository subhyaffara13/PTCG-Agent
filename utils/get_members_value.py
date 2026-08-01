
def get_members_value(context):
    for keyword in context.node.keywords:
        if keyword.arg == "members":
            arg = keyword.value
            if isinstance(arg, ast.Call):
                return {"Function": arg.func.id}
            else:
                value = arg.id if isinstance(arg, ast.Name) else arg
                return {"Other": value}


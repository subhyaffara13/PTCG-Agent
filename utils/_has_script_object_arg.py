
def _has_script_object_arg(schema: torch.FunctionSchema) -> bool:
    return any(isinstance(arg.type, torch.ClassType) for arg in schema.arguments)



def add_python_attr_to_scripted_model(script_model, orig, attr) -> None:
    if hasattr(orig, attr) and script_model_defines_attr(script_model, attr):
        setattr(script_model, attr, getattr(orig, attr))



def format_args_docstring(docstring: str, model_name: str) -> str:
    """
    Replaces placeholders such as {image_processor_class} in the docstring with the actual values,
    deducted from the model name and the auto modules.
    """
    # first check if there are any placeholders in the docstring, if not return it as is
    placeholders = set(_re_placeholders.findall(docstring))
    if not placeholders:
        return docstring

    # get the placeholders dictionary for the given model name
    placeholders_dict = get_placeholders_dict(placeholders, model_name)
    # replace the placeholders in the docstring with the values from the placeholders_dict
    for placeholder, value in placeholders_dict.items():
        if isinstance(value, dict) and placeholder == "image_processor_class":
            value = value.get("torchvision", value.get("pil", None))
        if placeholder is not None:
            docstring = docstring.replace(f"{{{placeholder}}}", value)
    return docstring


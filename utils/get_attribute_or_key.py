
def get_attribute_or_key(tool_or_function, attribute, default=None):
    if hasattr(tool_or_function, attribute):
        return getattr(tool_or_function, attribute)
    return tool_or_function.get(attribute, default)



def encoding_for_model(model_name: str) -> Encoding:
    """Returns the encoding used by a model.

    Raises a KeyError if the model name is not recognised.
    """
    return get_encoding(encoding_name_for_model(model_name))


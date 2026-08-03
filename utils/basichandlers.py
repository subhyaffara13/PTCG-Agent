import json

def basichandlers(extension: str, data):
    """Transforms raw data (byte stream) into python objects.

    Looks at the extension and loads the data into a python object supporting
    the corresponding extension.

    Args:
        extension (str): The file extension
        data (byte stream): Data to load into a python object.

    Returns:
        object: The data loaded into a corresponding python object
            supporting the extension.

    Example:
        >>> import pickle
        >>> data = pickle.dumps("some data")
        >>> new_data = basichandlers("pickle", data)
        >>> new_data
        some data

    The transformation of data for extensions are:
        - txt, text, transcript: utf-8 decoded data of str format
        - cls, cls2, class, count, index, inx, id: int
        - json, jsn: json loaded data
        - pickle, pyd: pickle loaded data
        - pt: torch loaded data
    """

    if extension in "txt text transcript":
        return data.decode("utf-8")

    if extension in ["cls", "cls2", "class", "count", "index", "inx", "id"]:
        try:
            return int(data)
        except ValueError:
            return None

    if extension in "json jsn":
        return json.loads(data)

    if extension in ["pyd", "pickle"]:
        return pickle.loads(data)

    if extension == "pt":
        stream = io.BytesIO(data)
        return torch.load(stream)

    # if extension in "ten tb".split():
    #     from . import tenbin
    #     return tenbin.decode_buffer(data)

    # if extension in "mp msgpack msg".split():
    #     import msgpack
    #     return msgpack.unpackb(data)

    return None


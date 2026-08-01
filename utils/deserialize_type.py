
def deserialize_type(data: JsonDict | str) -> Type:
    if isinstance(data, str):
        return Instance.deserialize(data)
    classname = data[".class"]
    method = deserialize_map.get(classname)
    if method is not None:
        return method(data)
    raise NotImplementedError(f"unexpected .class {classname}")


def deserialize_type(data: JsonDict | str, ctx: DeserMaps) -> RType:
    """Deserialize a JSON-serialized RType.

    Arguments:
        data: The decoded JSON of the serialized type
        ctx: The deserialization maps to use
    """
    # Since there are so few types, we just case on them directly.  If
    # more get added we should switch to a system like mypy.types
    # uses.
    if isinstance(data, str):
        if data in ctx.classes:
            return RInstance(ctx.classes[data])
        elif data in RPrimitive.primitive_map:
            return RPrimitive.primitive_map[data]
        elif data == "void":
            return RVoid()
        else:
            assert False, f"Can't find class {data}"
    elif data[".class"] == "RTuple":
        return RTuple.deserialize(data, ctx)
    elif data[".class"] == "RUnion":
        return RUnion.deserialize(data, ctx)
    elif data[".class"] == "RVec":
        return RVec.deserialize(data, ctx)
    raise NotImplementedError("unexpected .class {}".format(data[".class"]))


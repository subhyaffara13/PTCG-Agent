
def barbs(*args, data: DataParamType = None, **kwargs) -> Barbs:
    return gca().barbs(*args, **({"data": data} if data is not None else {}), **kwargs)


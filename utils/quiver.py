
def quiver(*args, data: DataParamType = None, **kwargs) -> Quiver:
    __ret = gca().quiver(
        *args, **({"data": data} if data is not None else {}), **kwargs
    )
    sci(__ret)
    return __ret


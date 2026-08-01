
def contourf(*args, data: DataParamType = None, **kwargs) -> QuadContourSet:
    __ret = gca().contourf(
        *args, **({"data": data} if data is not None else {}), **kwargs
    )
    if __ret._A is not None:  # type: ignore[attr-defined]
        sci(__ret)
    return __ret


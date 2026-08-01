
def clabel(CS: ContourSet, levels: ArrayLike | None = None, **kwargs) -> list[Text]:
    return gca().clabel(CS, levels=levels, **kwargs)


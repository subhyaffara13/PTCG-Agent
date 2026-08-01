
def stairs(
    values: ArrayLike,
    edges: ArrayLike | None = None,
    *,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    baseline: float | ArrayLike | None = 0,
    fill: bool = False,
    data: DataParamType = None,
    **kwargs,
) -> StepPatch:
    return gca().stairs(
        values,
        edges=edges,
        orientation=orientation,
        baseline=baseline,
        fill=fill,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )



def grouped_bar(
    heights: Sequence[ArrayLike] | dict[str, ArrayLike] | np.ndarray | pd.DataFrame,
    *,
    positions: ArrayLike | None = None,
    group_spacing: float | None = 1.5,
    bar_spacing: float | None = 0,
    tick_labels: Sequence[str] | None = None,
    labels: Sequence[str] | None = None,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    colors: Iterable[ColorType] | None = None,
    **kwargs,
) -> list[BarContainer]:
    return gca().grouped_bar(
        heights,
        positions=positions,
        group_spacing=group_spacing,
        bar_spacing=bar_spacing,
        tick_labels=tick_labels,
        labels=labels,
        orientation=orientation,
        colors=colors,
        **kwargs,
    )


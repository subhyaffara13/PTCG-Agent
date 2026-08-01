
def pie_label(
    container: PieContainer,
    /,
    labels: str | Sequence[str],
    *,
    distance: float = 0.6,
    textprops: dict | None = None,
    rotate: bool = False,
    alignment: str = "auto",
) -> list[Text]:
    return gca().pie_label(
        container,
        labels,
        distance=distance,
        textprops=textprops,
        rotate=rotate,
        alignment=alignment,
    )


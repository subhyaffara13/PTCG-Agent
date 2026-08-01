
def quiverkey(
    Q: Quiver, X: float, Y: float, U: float, label: str, **kwargs
) -> QuiverKey:
    return gca().quiverkey(Q, X, Y, U, label, **kwargs)


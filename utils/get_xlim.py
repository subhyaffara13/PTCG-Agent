
def get_xlim(lines: Iterable[Line2D]) -> tuple[float, float]:
    left, right = np.inf, -np.inf
    for line in lines:
        x = line.get_xdata(orig=False)
        left = min(np.nanmin(x), left)
        right = max(np.nanmax(x), right)
    return left, right


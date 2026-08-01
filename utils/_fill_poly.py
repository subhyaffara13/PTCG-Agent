
def _fill_poly(buf: list[list[Color | None]], verts: list[tuple[int, int]], color: Color) -> None:
    bh = len(buf)
    bw = len(buf[0]) if buf else 0
    all_y = [v[1] for v in verts]
    y0 = max(0, min(all_y))
    y1 = min(bh - 1, max(all_y))
    n = len(verts)
    for y in range(y0, y1 + 1):
        xl: float = float("inf")
        xr: float = float("-inf")
        for i in range(n):
            ax, ay = verts[i]
            bx, by = verts[(i + 1) % n]
            if ay == by:
                if y == ay:
                    xl = min(xl, float(min(ax, bx)))
                    xr = max(xr, float(max(ax, bx)))
                continue
            if not (min(ay, by) <= y <= max(ay, by)):
                continue
            t = (y - ay) / (by - ay)
            ix = ax + t * (bx - ax)
            xl = min(xl, ix)
            xr = max(xr, ix)
        if xl <= xr:
            for x in range(max(0, round(xl)), min(bw, round(xr) + 1)):
                buf[y][x] = color


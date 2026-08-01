
def _prepare_city_data(repos: list[RepoStorageInfo]) -> CityData:
    sorted_repos = sorted(repos, key=lambda r: r.storage, reverse=True)
    display = sorted_repos[:_MAX_TILES]
    extra_count = max(0, len(sorted_repos) - _MAX_TILES)
    extra_storage = sum(r.storage for r in sorted_repos[_MAX_TILES:])
    total_storage = sum(r.storage for r in repos)
    max_storage = max(1, display[0].storage)

    n = len(display) + (1 if extra_count > 0 else 0)
    cols = min(n, _COLS)
    rows = math.ceil(n / cols) if cols > 0 else 1

    tiles: list[TileInfo] = []
    for i, repo in enumerate(display):
        r, c = divmod(i, cols)
        h = max(_MIN_H, round(math.sqrt(repo.storage / max_storage) * _MAX_H))
        top, left, right = _TYPE_COLORS.get(repo.type, _EXTRA_COLORS)
        tiles.append(TileInfo(r, c, h, top, left, right, repo))
    if extra_count > 0:
        r, c = divmod(len(display), cols)
        h = max(_MIN_H, round(math.sqrt(extra_storage / max_storage) * _MAX_H))
        tiles.append(TileInfo(r, c, h, *_EXTRA_COLORS, None))

    r_lo, r_hi = -_EXT, rows - 1 + _EXT
    c_lo, c_hi = -_EXT, cols - 1 + _EXT

    xs: list[int] = []
    ys: list[int] = []
    for rr in range(r_lo, r_hi + 1):
        for cc in range(c_lo, c_hi + 1):
            cx, cy = (cc - rr) * _DX, (cc + rr) * _DY
            xs.extend([cx - _DX, cx + _DX])
            ys.extend([cy, cy + 2 * _DY])
    for tile in tiles:
        ys.append((tile.grid_col + tile.grid_row) * _DY - tile.height)

    x_off = -min(xs)
    y_off = -min(ys)
    buf_w = max(xs) - min(xs) + 1
    buf_h = max(ys) - min(ys) + 1
    if buf_h % 2:
        buf_h += 1

    return CityData(
        tiles=tiles,
        rows=rows,
        cols=cols,
        x_off=x_off,
        y_off=y_off,
        buf_w=buf_w,
        buf_h=buf_h,
        total_storage=total_storage,
        extra_count=extra_count,
        extra_storage=extra_storage,
        all_repos=repos,
    )


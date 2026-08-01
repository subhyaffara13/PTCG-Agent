
def _game_loop(city: CityData, cur_row: int, cur_col: int) -> None:
    tile_map: dict[tuple[int, int], TileInfo] = {(t.grid_row, t.grid_col): t for t in city.tiles}
    city = dataclasses.replace(city, buf_h=city.buf_h + _CURSOR_PAD, y_off=city.y_off + _CURSOR_PAD)
    base_buf = _render_base_buffer(city)

    summary = _build_summary(city.all_repos, city.total_storage, city.extra_count)

    # Intro: cursor drops onto starting tile
    tx, ty = _tile_top_center(city, cur_row, cur_col, tile_map)
    for i in range(1, _MOVE_FRAMES + 1):
        t = i / _MOVE_FRAMES
        t = t * t * (3 - 2 * t)
        drop_y = ty - 16 * (1 - t)
        frame = _copy_buf(base_buf)
        _highlight_tile(frame, city, tile_map[(cur_row, cur_col)])
        _draw_cursor(frame, tx, round(drop_y))
        _present(city, frame, tile_map.get((cur_row, cur_col)), summary)
        time.sleep(_MOVE_DELAY)

    while True:
        cx, cy = _tile_top_center(city, cur_row, cur_col, tile_map)
        frame = _copy_buf(base_buf)
        _highlight_tile(frame, city, tile_map[(cur_row, cur_col)])
        _draw_cursor(frame, cx, cy)
        _present(city, frame, tile_map.get((cur_row, cur_col)), summary)

        key = _read_key()
        if key in ("q", "Q", "esc", "\x03"):
            return

        dr, dc = _key_to_direction(key)
        if dr == 0 and dc == 0:
            continue

        nr, nc = cur_row + dr, cur_col + dc
        if (nr, nc) not in tile_map:
            continue

        ex, ey = _tile_top_center(city, nr, nc, tile_map)
        for i in range(1, _MOVE_FRAMES + 1):
            t = i / _MOVE_FRAMES
            t = t * t * (3 - 2 * t)
            bx = cx + (ex - cx) * t
            by = cy + (ey - cy) * t
            frame = _copy_buf(base_buf)
            _highlight_tile(frame, city, tile_map[(nr, nc)])
            _draw_cursor(frame, round(bx), round(by))
            _present(city, frame, tile_map.get((nr, nc)), summary)
            time.sleep(_MOVE_DELAY)

        cur_row, cur_col = nr, nc


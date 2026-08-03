import sys

def _present(req):
    return any(_dist_matches_req(dist, req) for dist in metadata.distributions())


def _present(
    city: CityData,
    buf: list[list[Color | None]],
    tile: TileInfo | None,
    summary: list[str],
) -> None:
    city_lines = _pixels_to_lines(buf)
    while city_lines and not _strip_ansi(city_lines[0]).strip():
        city_lines.pop(0)
    while city_lines and not _strip_ansi(city_lines[-1]).strip():
        city_lines.pop()

    city_w = max((_visible_len(line) for line in city_lines), default=0)
    term = shutil.get_terminal_size()
    panel_max_w = max(20, term.columns - city_w - _SUMMARY_W - 2 * _GAP)

    info = _build_info_panel(tile, city, panel_max_w)

    n = max(len(summary), len(city_lines), len(info))
    summary_lo = max(0, (n - len(summary)) // 2)
    info_lo = max(0, (n - len(info)) // 2)

    lines: list[str] = []
    for i in range(n):
        si = i - summary_lo
        lt = summary[si] if 0 <= si < len(summary) else ""
        lpad = max(0, _SUMMARY_W - _visible_len(lt))

        ct = city_lines[i] if i < len(city_lines) else ""
        cpad = max(0, city_w - _visible_len(ct))

        ri = i - info_lo
        rt = info[ri] if 0 <= ri < len(info) else ""

        lines.append(lt + " " * lpad + " " * _GAP + ct + " " * cpad + " " * _GAP + rt)

    lines.append("")
    lines.append("  \033[90mWASD/Arrows: move · Q/ESC: quit\033[0m")

    while len(lines) < term.lines - 1:
        lines.append("")

    output = "\033[H"
    for line in lines[: term.lines - 1]:
        output += line + "\033[K\r\n"
    sys.stdout.write(output)
    sys.stdout.flush()


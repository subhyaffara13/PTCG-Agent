
def _pixels_to_lines(buf: list[list[Color | None]]) -> list[str]:
    height = len(buf)
    width = len(buf[0]) if buf else 0
    lines: list[str] = []
    for row in range(0, height, 2):
        last = -1
        for col in range(width - 1, -1, -1):
            top = buf[row][col]
            bot = buf[row + 1][col] if row + 1 < height else None
            if top or bot:
                last = col
                break
        if last < 0:
            lines.append("")
            continue

        parts: list[str] = []
        cfg: Color | None = None
        cbg: Color | None = None

        for col in range(last + 1):
            top = buf[row][col]
            bot = buf[row + 1][col] if row + 1 < height else None

            if not top and not bot:
                if cfg is not None or cbg is not None:
                    parts.append("\033[0m")
                    cfg = cbg = None
                parts.append(" ")
                continue

            if top and bot and top == bot:
                nfg, nbg, ch = top, None, "█"
            elif top and bot:
                nfg, nbg, ch = bot, top, "▄"
            elif top:
                nfg, nbg, ch = top, None, "▀"
            else:
                nfg, nbg, ch = bot, None, "▄"  # type: ignore[assignment]

            esc = ""
            if nfg != cfg:
                esc += f"\033[38;2;{nfg[0]};{nfg[1]};{nfg[2]}m"
                cfg = nfg
            if nbg != cbg:
                esc += "\033[49m" if nbg is None else f"\033[48;2;{nbg[0]};{nbg[1]};{nbg[2]}m"
                cbg = nbg
            parts.append(esc + ch)

        if cfg is not None or cbg is not None:
            parts.append("\033[0m")
        lines.append("".join(parts))
    return lines


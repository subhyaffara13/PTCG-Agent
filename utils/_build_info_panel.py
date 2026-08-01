
def _build_info_panel(tile: TileInfo | None, city: CityData, max_w: int) -> list[str]:
    reset = "\033[0m"
    gray = "\033[90m"
    bold = "\033[1m"
    indent = "  "
    content_w = max_w - len(indent)

    lines: list[str] = [""]
    lines.append(f"{indent}{bold}City Explorer{reset}")
    lines.append(indent + "─" * min(22, content_w))
    lines.append("")

    if tile is None:
        lines.append(f"{indent}{gray}Move to a tile")
        lines.append(f"{indent}to see details.{reset}")
        return lines

    if tile.repo is None:
        lines.append(f"{indent}{gray}+{city.extra_count} more repos{reset}")
        lines.append(f"{indent}{gray}{format_size(city.extra_storage, human_readable=True)} combined{reset}")
        return lines

    repo = tile.repo
    name = repo.id
    if len(name) > content_w:
        name = name[: content_w - 3] + "..."
    lines.append(f"{indent}{bold}{name}{reset}")
    lines.append("")

    type_ansi = {
        "model": "\033[38;2;175;148;240m",
        "dataset": "\033[38;2;245;128;128m",
        "space": "\033[38;2;245;175;85m",
        "bucket": "\033[38;2;112;185;242m",
    }
    tc = type_ansi.get(repo.type, "")

    lines.append(f"{indent}Type       {tc}{repo.type}{reset}")
    lines.append(f"{indent}Visibility {repo.visibility}")
    lines.append(f"{indent}Storage    {format_size(repo.storage, human_readable=True)}")
    lines.append(f"{indent}Usage      {repo.storage_percent:.1f}%")
    lines.append("")

    bar_w = min(18, content_w)
    filled = max(0, min(bar_w, round(repo.storage_percent / 100 * bar_w)))
    lines.append(f"{indent}{tc}{'█' * filled}{gray}{'░' * (bar_w - filled)}{reset}")

    return lines



def format_decisions(dec_file: Path) -> str:
    content = dec_file.read_text(encoding="utf-8")
    entries = content.split("## Iteration ")
    if len(entries) <= 1:
        return "Decision log is empty."
    last_entries = entries[-3:]
    result_text = "**📝 Recent Decision Log Entries:**\n"
    for item in last_entries:
        result_text += f"\n*Iteration {item.strip()[:1000]}*\n"
    if len(result_text) > 2000:
        result_text = result_text[:1990] + "\n...(truncated)"
    return result_text


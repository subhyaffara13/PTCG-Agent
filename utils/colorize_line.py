
def colorize_line(linenum: str, s: str, hint_html: str) -> str:
    hint_prefix = " " * len(linenum) + "  "
    line_span = f'<div class="collapsible" style="background-color: #fcc">{linenum}  {s}</div>'
    hint_div = f'<div class="content">{hint_prefix}<div class="hint">{hint_html}</div></div>'
    return f"<span>{line_span}{hint_div}</span>"


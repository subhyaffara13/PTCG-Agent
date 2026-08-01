
def get_line_rate(covered_lines: int, total_lines: int) -> str:
    if total_lines == 0:
        return str(1.0)
    else:
        return f"{covered_lines / total_lines:.4f}"



def _report_free(free_external, free_internal):
    total = free_external + free_internal
    suffix = ""
    if total != 0:
        pct = (free_internal / total) * 100
        suffix = f" ({pct:.1f}% internal)"
    return f"{Bytes(total)}{suffix}"


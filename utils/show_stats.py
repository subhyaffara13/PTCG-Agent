
def show_stats(response: Mapping[str, object]) -> None:
    for key, value in sorted(response.items()):
        if key in ("out", "err", "stdout", "stderr"):
            # Special case text output to display just 40 characters of text
            value = repr(value)[1:-1]
            if len(value) > 50:
                value = f"{value[:40]} ... {len(value)-40} more characters"
            print("%-24s: %s" % (key, value))
            continue
        print("%-24s: %10s" % (key, "%.3f" % value if isinstance(value, float) else value))


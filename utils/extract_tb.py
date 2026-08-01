
def extract_tb(tb: TracebackType | None, limit: int | None = None) -> StackSummary:
    if tb is None:
        return traceback.StackSummary.from_list([])
    # pyrefly: ignore [implicit-any]
    frame_summary = []
    while tb is not None:
        if limit:
            if len(frame_summary) < limit:
                frame_summary.append(
                    # pyrefly: ignore[missing-attribute]
                    tb.frame_summary
                )
            else:
                break
        else:
            frame_summary.append(tb.frame_summary)  # pyrefly: ignore[missing-attribute]
        tb = tb.tb_next
    return traceback.StackSummary.from_list(frame_summary)


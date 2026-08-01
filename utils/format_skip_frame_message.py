
def format_skip_frame_message(code: types.CodeType | None, reason: str) -> str:
    if code is not None:
        frame_info = format_frame_info(code)
        return (
            f"torch.compile intentionally decided to skip the frame {frame_info} and fall back to eager.\n"
            f"Reason: {reason}"
        )
    else:
        return (
            f"torch.compile intentionally decided to skip the frame and fall back to eager.\n"
            f"Reason: {reason}"
        )


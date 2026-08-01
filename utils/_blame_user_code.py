
def _blame_user_code(e: Exception, frame: types.FrameType) -> None:
    frame_summary = traceback.FrameSummary(
        frame.f_code.co_filename,
        frame.f_lineno,
        frame.f_code.co_name,
    )
    msg = e.args[0]
    msg += "\n\nThe following call raised this error:\n" + "".join(
        traceback.StackSummary.from_list([frame_summary]).format()
    )
    e.args = (msg,)


import os

def _find_user_code_frame() -> types.FrameType | None:
    frame = inspect.currentframe()
    while frame is not None:
        if not frame.f_code.co_filename.startswith(
            os.path.dirname(inspect.getfile(torch)) + os.path.sep
        ):
            break
        frame = frame.f_back
    return frame



def _summarize_frame(frame: Frame) -> str:
  if frame.start_column != 0:
    return (f"{frame.file_name}:{frame.start_line}:{frame.start_column} "
            f"({frame.function_name})")
  else:
    return f"{frame.file_name}:{frame.start_line} ({frame.function_name})"



def _make_logging_record(level):
  si = source_info_util.current()
  user_frame = source_info_util.user_frame(si.traceback)

  file_name = "(unknown file)"
  line_no = 0
  if user_frame:
    file_name = user_frame.file_name
    line_no = user_frame.start_line
  args = ()
  return logger.makeRecord(
      logger.name, level, file_name, line_no, "", args, None
  )



def raw_frame_to_frame(code: types.CodeType, lasti: int) -> Frame:
  loc = xla_client.Traceback.code_addr2location(code, lasti)
  start_line, start_column, end_line, end_column = loc
  return Frame(file_name=code.co_filename,
              function_name=code.co_qualname,
              start_line=start_line, start_column=start_column,
              end_line=end_line, end_column=end_column)


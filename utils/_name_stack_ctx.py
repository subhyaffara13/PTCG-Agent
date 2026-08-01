
def _name_stack_ctx(src_info):
  stack = source_info_util.current_name_stack() + src_info.name_stack
  return source_info_util.user_context(src_info.traceback, name_stack=stack)


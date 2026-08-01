
def string_flag(name, default, *args, **kwargs) -> Flag[str]:
  update_hook = kwargs.pop("update_hook", None)
  holder = Flag(name, default, update_hook)
  config.add_option(name, holder, str, args, kwargs)
  return holder


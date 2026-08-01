
def float_flag(name, default, *args, **kwargs) -> Flag[float]:
  update_hook = kwargs.pop("update_hook", None)
  holder = Flag(name, default, update_hook)
  config.add_option(name, holder, float, args, kwargs)
  return holder


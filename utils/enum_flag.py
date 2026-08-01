
def enum_flag(name, default, *args, **kwargs) -> Flag[str]:
  update_hook = kwargs.pop("update_hook", None)
  holder = Flag(name, default, update_hook)
  config.add_option(name, holder, 'enum', args, kwargs)
  return holder



def new_name_stack(name: str = '') -> NameStack:
  name_stack = NameStack()
  if name:
    name_stack = name_stack.extend(name)
  return name_stack


from typing import Union

def _get_args_type(
    args: Union[Type[CheckpointArgs], CheckpointArgs],
) -> type[CheckpointArgs]:
  if isinstance(args, type):
    return args
  else:
    return type(args)


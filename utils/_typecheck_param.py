import os

def _typecheck_param(prim, param, name, msg_required, pred):
  if not pred:
    msg = (f'invalid {prim} param {name} of type {type(param).__name__}, '
           f'{msg_required} required:')
    param_str = str(param)
    # Avoid using os.linesep here to have the same multi-line error message
    # format on different platforms.
    sep = os.linesep if '\n' in param_str or '\r' in param_str else ' '
    msg = sep.join([msg, param_str])
    raise core.JaxprTypeError(msg)


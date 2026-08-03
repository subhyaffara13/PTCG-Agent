import copy
import sys

def _format_print_callback(
    fmt: str, np_printoptions, has_placeholders, logging_record, *args, **kwargs
):
  if has_placeholders:
    with np.printoptions(**np_printoptions):
      msg = fmt.format(*args, **kwargs)
  else:
    assert not kwargs, "Format without placeholders should not have kwargs."
    msg = " ".join((fmt, *(str(a) for a in args)))
  if logging_record:
    logging_record = copy.copy(logging_record)
    logging_record.msg = msg
    logger.handle(logging_record)
  else:
    sys.stdout.write(msg + "\n")


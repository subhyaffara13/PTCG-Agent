import sys

def _ReraiseTypeErrorWithFieldName(message_name, field_name):
  """Re-raise the currently-handled TypeError with the field name added."""
  exc = sys.exc_info()[1]
  if len(exc.args) == 1 and type(exc) is TypeError:
    # simple TypeError; add field name to exception message
    exc = TypeError('%s for field %s.%s' % (str(exc), message_name, field_name))

  # re-raise possibly-amended exception with original traceback:
  raise exc.with_traceback(sys.exc_info()[2])


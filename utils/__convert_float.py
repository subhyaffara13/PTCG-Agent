import math


def _ConvertFloat(value, field):
  """Convert an floating point number."""
  if isinstance(value, float):
    if math.isnan(value):
      raise ParseError('Couldn\'t parse NaN, use quoted "NaN" instead')
    if math.isinf(value):
      if value > 0:
        raise ParseError(
            "Couldn't parse Infinity or value too large, "
            'use quoted "Infinity" instead'
        )
      else:
        raise ParseError(
            "Couldn't parse -Infinity or value too small, "
            'use quoted "-Infinity" instead'
        )
    if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_FLOAT:
      # pylint: disable=protected-access
      if value > type_checkers._FLOAT_MAX:
        raise ParseError('Float value too large')
      # pylint: disable=protected-access
      if value < type_checkers._FLOAT_MIN:
        raise ParseError('Float value too small')
  if value == 'nan':
    raise ParseError('Couldn\'t parse float "nan", use "NaN" instead')
  try:
    # Assume Python compatible syntax.
    return float(value)
  except ValueError as e:
    # Check alternative spellings.
    if value == _NEG_INFINITY:
      return float('-inf')
    elif value == _INFINITY:
      return float('inf')
    elif value == _NAN:
      return float('nan')
    else:
      raise ParseError("Couldn't parse float: {0}".format(value)) from e


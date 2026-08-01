
def _format_parameter_list(testcase_params):
  if isinstance(testcase_params, abc.Mapping):
    return ', '.join('%s=%s' % (argname, _clean_repr(value))
                     for argname, value in testcase_params.items())
  elif _non_string_or_bytes_iterable(testcase_params):
    return ', '.join(map(_clean_repr, testcase_params))
  else:
    return _format_parameter_list((testcase_params,))


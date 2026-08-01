
def _modify_class(class_object, testcases, naming_type):
  assert not getattr(class_object, '_test_params_reprs', None), (
      'Cannot add parameters to %s. Either it already has parameterized '
      'methods, or its super class is also a parameterized class.' % (
          class_object,))
  # NOTE: _test_params_repr is private to parameterized.TestCase and it's
  # metaclass; do not use it outside of those classes.
  class_object._test_params_reprs = test_params_reprs = {}
  for name, obj in class_object.__dict__.copy().items():
    if (name.startswith(unittest.TestLoader.testMethodPrefix)
        and isinstance(obj, types.FunctionType)):
      delattr(class_object, name)
      methods = {}
      _update_class_dict_for_param_test_case(
          class_object.__name__, methods, test_params_reprs, name,
          _ParameterizedTestIter(obj, testcases, naming_type, name))
      for meth_name, meth in methods.items():
        setattr(class_object, meth_name, meth)



def skipThisClass(
    reason: str,
) -> abc.Callable[[type[_T]], type[_T]]:
  """Skip tests in the decorated TestCase, but not any of its subclasses.

  This decorator indicates that this class should skip all its tests, but not
  any of its subclasses. Useful for if you want to share testMethod or setUp
  implementations between a number of concrete testcase classes.

  Example usage, showing how you can share some common test methods between
  subclasses. In this example, only ``BaseTest`` will be marked as skipped, and
  not RealTest or SecondRealTest::

      @absltest.skipThisClass("Shared functionality")
      class BaseTest(absltest.TestCase):
        def test_simple_functionality(self):
          self.assertEqual(self.system_under_test.method(), 1)

      class RealTest(BaseTest):
        def setUp(self):
          super().setUp()
          self.system_under_test = MakeSystem(argument)

        def test_specific_behavior(self):
          ...

      class SecondRealTest(BaseTest):
        def setUp(self):
          super().setUp()
          self.system_under_test = MakeSystem(other_arguments)

        def test_other_behavior(self):
          ...

  Args:
    reason: The reason we have a skip in place. For instance: 'shared test
      methods' or 'shared assertion methods'.

  Returns:
    Decorator function that will cause a class to be skipped.
  """
  if isinstance(reason, type):
    raise TypeError(f'Got {reason!r}, expected reason as string')

  def _skip_class(test_case_class):
    if not issubclass(test_case_class, unittest.TestCase):
      raise TypeError(
          f'Decorating {test_case_class!r}, expected TestCase subclass'
      )

    # Only shadow the setUpClass method if it is directly defined. If it is
    # in the parent class we invoke it via a super() call instead of holding
    # a reference to it.
    shadowed_setupclass = test_case_class.__dict__.get('setUpClass', None)

    @classmethod
    def replacement_setupclass(cls, *args, **kwargs):
      # Skip this class if it is the one that was decorated with @skipThisClass
      if cls is test_case_class:
        raise SkipTest(reason)
      if shadowed_setupclass:
        # Pass along `cls` so the MRO chain doesn't break.
        # The original method is a `classmethod` descriptor, which can't
        # be directly called, but `__func__` has the underlying function.
        return shadowed_setupclass.__func__(cls, *args, **kwargs)
      else:
        # Because there's no setUpClass() defined directly on test_case_class,
        # we call super() ourselves to continue execution of the inheritance
        # chain.
        return super(test_case_class, cls).setUpClass(*args, **kwargs)

    test_case_class.setUpClass = replacement_setupclass
    return test_case_class

  return _skip_class


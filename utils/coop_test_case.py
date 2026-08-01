
def CoopTestCase(other_base_class) -> type:  # pylint: disable=invalid-name, g-bare-generic
  """Returns a new base class with a cooperative metaclass base.

  This enables the TestCase to be used in combination
  with other base classes that have custom metaclasses, such as
  ``mox.MoxTestBase``.

  Only works with metaclasses that do not override ``type.__new__``.

  Example::

      from absl.testing import parameterized

      class ExampleTest(parameterized.CoopTestCase(OtherTestCase)):
        ...

  Args:
    other_base_class: (class) A test case base class.

  Returns:
    A new class object.
  """
  # If the other base class has a metaclass of 'type' then trying to combine
  # the metaclasses will result in an MRO error. So simply combine them and
  # return.
  if type(other_base_class) == type:  # pylint: disable=unidiomatic-typecheck
    warnings.warn(
        'CoopTestCase is only necessary when combining with a class that uses'
        ' a metaclass. Use multiple inheritance like this instead: class'
        f' ExampleTest(paramaterized.TestCase, {other_base_class.__name__}):',
        stacklevel=2,
    )

    class CoopTestCaseBase(other_base_class, TestCase):
      pass

    return CoopTestCaseBase
  else:

    class CoopMetaclass(type(other_base_class), TestGeneratorMetaclass):  # type: ignore  # pylint: disable=unused-variable
      pass

    class CoopTestCaseBase(other_base_class, TestCase, metaclass=CoopMetaclass):  # type: ignore
      pass

    return CoopTestCaseBase


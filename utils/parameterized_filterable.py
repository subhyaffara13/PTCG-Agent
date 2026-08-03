from typing import Any, Callable

def parameterized_filterable(*,
    kwargs: Sequence[dict[str, Any]],
    testcase_name: Callable[[dict[str, Any]], str] | None = None,
    one_containing: str | None = None,
):
  """Decorator for named parameterized tests, with filtering support.

  Works like ``parameterized.named_parameters``, except that it sanitizes the test
  names so that we can use ``pytest -k`` and ``python test.py -k`` test filtering.
  This means, e.g., that many special characters are replaced with `_`.
  It also supports the ``one_containing`` arg to select one of the tests, while
  leaving the name unchanged, which is useful for IDEs to be able to easily
  pick up the enclosing test name.

  Usage:
     @jtu.parameterized_filterable(
       # one_containing="a_4",
       [dict(a=4, b=5),
        dict(a=5, b=4)])
     def test_my_test(self, *, a, b): ...

  Args:
    kwargs: Each entry is a set of kwargs to be passed to the test function.
    testcase_name: Optionally, a function to construct the testcase_name from
      one kwargs dict. If not given then ``kwargs`` may contain ``testcase_name`` and
      otherwise the test case name is constructed as ``str(kwarg)``.
      We sanitize the test names to work with -k test filters. See
      ``sanitize_test_name``.
    one_containing: If given, then leaves the test name unchanged, and use
      only one of the ``kwargs`` whose `testcase_name` includes ``one_containing``.
  """
  # Ensure that all kwargs contain a testcase_name
  kwargs_with_testcase_name: Sequence[dict[str, Any]]
  if testcase_name is not None:
    kwargs_with_testcase_name = [
      dict(testcase_name=sanitize_test_name(str(testcase_name(kw))), **kw)
      for kw in kwargs]
  else:
    for kw in kwargs:
      kw_testcase_name = kw.get("testcase_name")
      if kw_testcase_name is None:
        kw_testcase_name = "_".join(f"{k}={kw[k]}" for k in sorted(kw))
      kw["testcase_name"] = sanitize_test_name(kw_testcase_name)

    kwargs_with_testcase_name = kwargs
  if one_containing is not None:
    filtered = tuple(kw for kw in kwargs_with_testcase_name
                     if one_containing in kw["testcase_name"])
    assert filtered, (
      f"No testcase_name contains '{one_containing}'. "
      "The testcase_name values are\n  " +
      "\n  ".join(kw["testcase_name"] for kw in kwargs_with_testcase_name))
    kw = filtered[0]
    kw["testcase_name"] = ""
    return parameterized.named_parameters([kw])
  else:
    return parameterized.named_parameters(*kwargs_with_testcase_name)


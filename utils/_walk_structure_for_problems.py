
def _walk_structure_for_problems(
    a, b, aname, bname, problem_list, leaf_assert_equal_func, failure_exception
):
  """The recursive comparison behind assertSameStructure."""
  if type(a) != type(b) and not (  # pylint: disable=unidiomatic-typecheck
      _are_both_of_integer_type(a, b) or _are_both_of_sequence_type(a, b) or
      _are_both_of_set_type(a, b) or _are_both_of_mapping_type(a, b)):
    # We do not distinguish between int and long types as 99.99% of Python 2
    # code should never care.  They collapse into a single type in Python 3.
    problem_list.append('%s is a %r but %s is a %r' %
                        (aname, type(a), bname, type(b)))
    # If they have different types there's no point continuing
    return

  if isinstance(a, abc.Set):
    for k in a:
      if k not in b:
        problem_list.append(
            '%s has %r but %s does not' % (aname, k, bname))
    for k in b:
      if k not in a:
        problem_list.append('%s lacks %r but %s has it' % (aname, k, bname))

  # NOTE: a or b could be a defaultdict, so we must take care that the traversal
  # doesn't modify the data.
  elif isinstance(a, abc.Mapping):
    for k in a:
      if k in b:
        _walk_structure_for_problems(
            a[k], b[k], '%s[%r]' % (aname, k), '%s[%r]' % (bname, k),
            problem_list, leaf_assert_equal_func, failure_exception)
      else:
        problem_list.append(
            "%s has [%r] with value %r but it's missing in %s" %
            (aname, k, a[k], bname))
    for k in b:
      if k not in a:
        problem_list.append(
            '%s lacks [%r] but %s has it with value %r' %
            (aname, k, bname, b[k]))

  # Strings/bytes are Sequences but we'll just do those with regular !=
  elif (isinstance(a, abc.Sequence) and
        not isinstance(a, _TEXT_OR_BINARY_TYPES)):
    minlen = min(len(a), len(b))
    for i in range(minlen):
      _walk_structure_for_problems(
          a[i], b[i], '%s[%d]' % (aname, i), '%s[%d]' % (bname, i),
          problem_list, leaf_assert_equal_func, failure_exception)
    for i in range(minlen, len(a)):
      problem_list.append('%s has [%i] with value %r but %s does not' %
                          (aname, i, a[i], bname))
    for i in range(minlen, len(b)):
      problem_list.append('%s lacks [%i] but %s has it with value %r' %
                          (aname, i, bname, b[i]))

  else:
    try:
      leaf_assert_equal_func(a, b)
    except failure_exception:
      problem_list.append('%s is %r but %s is %r' % (aname, a, bname, b))


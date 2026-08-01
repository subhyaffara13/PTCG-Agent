
def product(*iterables, repeat=1, total=None, tqdm_class=tqdm_auto, **kwargs):
    """Equivalent of `itertools.product`."""
    if total is None:
        try:
            lens = list(map(len, iterables))
        except (TypeError, AttributeError):
            pass
        else:
            total = math.prod(lens) ** repeat
    yield from tqdm_class(itertools.product(*iterables, repeat=repeat), total=total, **kwargs)


def product(it: Iterable[T]) -> int:
    return functools.reduce(operator.mul, it, 1)


def product(a: IntTuple) -> int:
    if is_tuple(a):
        return reduce(lambda val, elem: val * product(elem), a, 1)
    else:
        return a


def product(*args, **kwargs):
    r"""
    Compute the product.

    Explanation
    ===========

    The notation for symbols is similar to the notation used in Sum or
    Integral. product(f, (i, a, b)) computes the product of f with
    respect to i from a to b, i.e.,

    ::

                                     b
                                   _____
        product(f(n), (i, a, b)) = |   | f(n)
                                   |   |
                                   i = a

    If it cannot compute the product, it returns an unevaluated Product object.
    Repeated products can be computed by introducing additional symbols tuples::

    Examples
    ========

    >>> from sympy import product, symbols
    >>> i, n, m, k = symbols('i n m k', integer=True)

    >>> product(i, (i, 1, k))
    factorial(k)
    >>> product(m, (i, 1, k))
    m**k
    >>> product(i, (i, 1, k), (k, 1, n))
    Product(factorial(k), (k, 1, n))

    """

    prod = Product(*args, **kwargs)

    if isinstance(prod, Product):
        return prod.doit(deep=False)
    else:
        return prod


def product(*kwargs_seqs, **testgrid):
  """A decorator for running tests over cartesian product of parameters values.

  See the module docstring for a usage example. The test will be run for every
  possible combination of the parameters.

  Args:
    *kwargs_seqs: Each positional parameter is a sequence of keyword arg dicts;
      every test case generated will include exactly one kwargs dict from each
      positional parameter; these will then be merged to form an overall list
      of arguments for the test case.
    **testgrid: A mapping of parameter names and their possible values. Possible
      values should given as either a list or a tuple.

  Raises:
    NoTestsError: Raised when the decorator generates no tests.

  Returns:
     A test generator to be handled by TestGeneratorMetaclass.
  """

  for name, values in testgrid.items():
    assert isinstance(values, (list, tuple)), (
        'Values of {} must be given as list or tuple, found {}'.format(
            name, type(values)))

  prior_arg_names = set()
  for kwargs_seq in kwargs_seqs:
    assert ((isinstance(kwargs_seq, (list, tuple))) and
            all(isinstance(kwargs, dict) for kwargs in kwargs_seq)), (
                'Positional parameters must be a sequence of keyword arg'
                'dicts, found {}'
                .format(kwargs_seq))
    if kwargs_seq:
      arg_names = set(kwargs_seq[0])
      assert all(set(kwargs) == arg_names for kwargs in kwargs_seq), (
          'Keyword argument dicts within a single parameter must all have the '
          'same keys, found {}'.format(kwargs_seq))
      assert not (arg_names & prior_arg_names), (
          'Keyword argument dict sequences must all have distinct argument '
          'names, found duplicate(s) {}'
          .format(sorted(arg_names & prior_arg_names)))
      prior_arg_names |= arg_names

  assert not (prior_arg_names & set(testgrid)), (
      'Arguments supplied in kwargs dicts in positional parameters must not '
      'overlap with arguments supplied as named parameters; found duplicate '
      'argument(s) {}'.format(sorted(prior_arg_names & set(testgrid))))

  # Convert testgrid into a sequence of sequences of kwargs dicts and combine
  # with the positional parameters.
  # So foo=[1,2], bar=[3,4] --> [[{foo: 1}, {foo: 2}], [{bar: 3, bar: 4}]]
  testgrid = (tuple({k: v} for v in vs) for k, vs in testgrid.items())
  testgrid = tuple(kwargs_seqs) + tuple(testgrid)

  # Create all possible combinations of parameters as a cartesian product
  # of parameter values.
  testcases = [
      dict(itertools.chain.from_iterable(case.items()
                                         for case in cases))
      for cases in itertools.product(*testgrid)
  ]
  return _parameter_decorator(_ARGUMENT_REPR, testcases)


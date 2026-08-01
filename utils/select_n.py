
def select_n(which: ArrayLike, *cases: ArrayLike) -> Array:
  """Selects array values from multiple cases.

  Generalizes XLA's `Select
  <https://www.openxla.org/xla/operation_semantics#select>`_
  operator. Unlike XLA's version, the operator is variadic and can select
  from many cases using an integer `pred`.

  Args:
    which: determines which case should be returned. Must be an array containing
      either a boolean or integer values. May either be a scalar or have
      shape matching ``cases``. For each array element, the value of ``which``
      determines which of ``cases`` is taken. ``which`` must be in the range
      ``[0 .. len(cases))``; for values outside that range the behavior is
      implementation-defined.
    *cases: a non-empty list of array cases. All must have equal dtypes and
      equal shapes.
  Returns:
    An array with shape and dtype equal to the cases, whose values are chosen
    according to ``which``.
  """
  if len(cases) == 0:
    raise ValueError("select_n() must have at least one case")
  which_pvary, *cases_pvary = core.auto_insert_reshard(which, *cases)
  return select_n_p.bind(which_pvary, *cases_pvary)


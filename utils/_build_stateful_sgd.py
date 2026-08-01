
def _build_stateful_sgd():
  # This SGD behaves like _build_sgd but also tests the optimizer state. The
  # momentum is set to zero rather than None so that the momentum terms are
  # calculated, but do not change the results.
  return alias.sgd(1.0, momentum=0.0)


def _build_stateful_sgd():
  # This SGD behaves like _build_sgd but also tests the optimizer state. The
  # momentum is set to zero rather than None so that the momentum terms are
  # calculated, but do not change the results.
  return alias.sgd(1.0, momentum=0.0)


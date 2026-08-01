
def keep(request):
    """
    Valid values for the 'keep' parameter used in
    .duplicated or .drop_duplicates
    """
    return request.param


def keep(keeps, xs):
  return [x for x, k in zip(xs, keeps) if k]


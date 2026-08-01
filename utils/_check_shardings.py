
def _check_shardings(shardings):
  if len(shardings) != 4:
    msg = f"shardings should container 4 inputs, but got {len(shardings)}"
    raise TypeError(msg)
  lhs, rhs, _, _ = shardings
  if len(lhs.spec) != 3 or len(rhs.spec) != 3:
    msg = (f'shardings specs rank should be 3, but got lhs: {len(lhs.spec)} '
            'and rhs: {len(rhs.spec)}')
    raise TypeError(msg)
  if lhs.spec[0] != rhs.spec[0]:
    msg = ('shardings spec for batch dim should be same, but got lhs: '
            '{lhs.spec[0]} and rhs: {rhs.spec[0]}')
    raise TypeError(msg)


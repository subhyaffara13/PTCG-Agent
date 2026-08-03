import itertools

def _enumerate_feasible_logical_axis_assignments(
    physical_mesh_shape: Sequence[int],
    assignment: np.ndarray,
    logical_axis_size: int,
) -> Generator[np.ndarray, None, None]:
  """Yields feasible assignments for a single logical axis.

  For a physical mesh of shape [x_1, ..., x_n], and the product of all previous
  assignments on each physical axes [y_1, ..., y_n], this function yields all
  possible assignments for the axis as 1-d arrays [z_1, ..., z_n], so that:

  - prod(z_1, ..., z_n) = logical_axis_size

  - x_i % (z_i * y_i) = 0

  Args:
    physical_mesh_shape: Physical mesh shape.
    assignment: Existing assignment matrix.
    logical_axis_size: Size of the logical axis to assign.

  Yields:
    All valid assignments for the logical axis. Each assignment is represented
    as an integer array of length len(physical_mesh_shape).
  """
  logical_axis_factors: MutableMapping[int, int] = collections.defaultdict(int)
  for factor in _get_prime_factors(logical_axis_size):
    logical_axis_factors[factor] += 1

  available_physical_mesh_shape = np.array(physical_mesh_shape) // np.prod(
      assignment, axis=-1
  )

  # To enable efficient enumerations, we first index physical axes by their
  # prime factors. Since we know the prime factorization of the logical axis
  # size, we could simply enumerate by picking the correct count for each
  # prime factor.
  physical_axes_by_factor: MutableMapping[int, list[int]] = (
      collections.defaultdict(list)
  )
  for physical_axis, physical_axis_size in enumerate(
      available_physical_mesh_shape
  ):
    for factor in _get_prime_factors(physical_axis_size):
      if factor not in logical_axis_factors:
        continue
      physical_axes_by_factor[factor].append(physical_axis)

  factors = []
  assignments_by_factor = []
  for factor, multiplicity in logical_axis_factors.items():
    factors.append(factor)
    assignments_by_factor.append(
        set(
            itertools.combinations(
                physical_axes_by_factor[factor], multiplicity
            )
        )
    )

  for axis_assignment in itertools.product(*assignments_by_factor):
    result = np.ones([len(physical_mesh_shape)], dtype=np.int64)
    for factor_index, per_factor_assignment in enumerate(axis_assignment):
      for physical_axis in per_factor_assignment:
        result[physical_axis] *= factors[factor_index]
    yield result


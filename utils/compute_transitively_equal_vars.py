
def compute_transitively_equal_vars(
    system: ConstraintSystem,
) -> dict[Variable, list[Variable]]:
  """Computes all transitively equal variables in a constraint system.

  The output dictionary maps each variable that appears in constraints in the
  constraint system to all the variables it is transitively equal to.
  """
  # The equality relations between variables form a graph where variables are
  # nodes and a constraint `v1 == v2` forms an edge. All variables in a
  # connected component are transitively equal. We use a Union-Find data
  # structure with path compression to efficiently find these connected
  # components (i.e., equivalence classes).
  parent: dict[Variable, Variable] = {}
  def find(v: Variable) -> Variable:
    if v not in parent:
      parent[v] = v
    if parent[v] != v:
      parent[v] = find(parent[v])
    return parent[v]

  def union(v1: Variable, v2: Variable):
    root1 = find(v1)
    root2 = find(v2)
    if root1 != root2:
      parent[root2] = root1

  all_vars: set[Variable] = set()
  for constraint in system.constraints:
    match constraint:
      case Equals(lhs=Variable() as lhs, rhs=Variable() as rhs):
        all_vars.add(lhs)
        all_vars.add(rhs)
        union(lhs, rhs)

  # Group variables by their component representative.
  components: dict[Variable, list[Variable]] = {}
  for v in sorted(all_vars, key=str):
    root = find(v)
    components.setdefault(root, []).append(v)

  equal_vars: dict[Variable, list[Variable]] = {}
  for component_vars in components.values():
    for v in component_vars:
      equal_vars[v] = [other for other in component_vars if other != v]

  return equal_vars


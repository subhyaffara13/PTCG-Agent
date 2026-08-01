
def generate_flatten_constraints(
    start_dim: int, end_dim: int, input: TVar, flattened: TVar, n: int, counter: int
) -> tuple[Conj, int]:
    d, counter = gen_tensor_dims(n, counter)
    c1 = BinConstraintT(input, TensorType(d), op_eq)
    start_dim = n if start_dim == -1 else abs(start_dim)
    end_dim = n + end_dim + 1 if end_dim < 0 else end_dim + 1
    c2 = CalcProduct(start_dim, end_dim, flattened, d)
    nat_constraints = gen_nat_constraints(d)
    return Conj([c1, c2, *nat_constraints]), counter


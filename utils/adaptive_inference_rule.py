
def adaptive_inference_rule(
    n: Node,
    module_instance: torch.nn.AdaptiveAvgPool2d,
    symbols: _SymbolDict,
    constraints: list[Constraint],
    counter: int,
) -> tuple[list[Constraint], int]:
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")

    avg_pool, counter = gen_tvar(counter)

    symbols[n] = avg_pool
    input_var = symbols[n.args[0]]

    # dim vars
    d1, counter = gen_dvar(counter)
    d2, counter = gen_dvar(counter)
    d3, counter = gen_dvar(counter)
    d4, counter = gen_dvar(counter)
    nat_constraints = gen_nat_constraints([d1, d2, d3, d4])
    c1 = BinConstraintT(input_var, TensorType([d1, d2, d3, d4]), op_matching)
    c2 = BinConstraintT(
        avg_pool,
        TensorType(
            [
                d1,
                d2,
                module_instance.output_size[  # pyrefly: ignore[bad-index, unsupported-operation]
                    0
                ],
                module_instance.output_size[  # pyrefly: ignore[bad-index, unsupported-operation]
                    1
                ],
            ]
        ),
        op_eq,
    )

    return [c1, c2, *nat_constraints], counter


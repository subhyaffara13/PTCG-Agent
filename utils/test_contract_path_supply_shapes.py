
def test_contract_path_supply_shapes() -> None:
    eq = "ab,bc,cd"
    shps = [(2, 3), (3, 4), (4, 5)]
    contract_path(eq, *shps, shapes=True)



def test_optimizer_registration() -> None:
    def custom_optimizer(
        inputs: List[ArrayIndexType], output: ArrayIndexType, size_dict: Dict[str, int], memory_limit: Optional[int]
    ) -> PathType:
        return [(0, 1)] * (len(inputs) - 1)

    with pytest.raises(KeyError):
        oe.paths.register_path_fn("optimal", custom_optimizer)

    oe.paths.register_path_fn("custom", custom_optimizer)
    assert "custom" in oe.paths._PATH_OPTIONS

    eq = "ab,bc,cd"
    shapes = [(2, 3), (3, 4), (4, 5)]
    path, _ = oe.contract_path(eq, *shapes, shapes=True, optimize="custom")  # type: ignore
    assert path == [(0, 1), (0, 1)]
    del oe.paths._PATH_OPTIONS["custom"]


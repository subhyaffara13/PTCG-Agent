from typing import Dict, List, Optional

def test_custom_path_optimizer() -> None:
    np = pytest.importorskip("numpy")

    class NaiveOptimizer(oe.paths.PathOptimizer):
        def __call__(
            self,
            inputs: List[ArrayIndexType],
            output: ArrayIndexType,
            size_dict: Dict[str, int],
            memory_limit: Optional[int] = None,
        ) -> PathType:
            self.was_used = True
            return [(0, 1)] * (len(inputs) - 1)

    eq, shapes = rand_equation(5, 3, seed=42, d_max=3)
    views = list(map(np.ones, shapes))

    exp = oe.contract(eq, *views, optimize=False)

    optimizer = NaiveOptimizer()
    out = oe.contract(eq, *views, optimize=optimizer)
    assert exp == out
    assert optimizer.was_used


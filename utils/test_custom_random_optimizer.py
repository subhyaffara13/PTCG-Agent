from typing import Any, Dict, List

def test_custom_random_optimizer() -> None:
    np = pytest.importorskip("numpy")

    class NaiveRandomOptimizer(oe.path_random.RandomOptimizer):
        @staticmethod
        def random_path(
            r: int, n: int, inputs: List[ArrayIndexType], output: ArrayIndexType, size_dict: Dict[str, int]
        ) -> Any:
            """Picks a completely random contraction order."""
            np.random.seed(r)
            ssa_path: List[TensorShapeType] = []
            remaining = set(range(n))
            while len(remaining) > 1:
                i, j = np.random.choice(list(remaining), size=2, replace=False)
                remaining.add(n + len(ssa_path))
                remaining.remove(i)
                remaining.remove(j)
                ssa_path.append((i, j))
            cost, size = oe.path_random.ssa_path_compute_cost(ssa_path, inputs, output, size_dict)
            return ssa_path, cost, size

        def setup(self, inputs: Any, output: Any, size_dict: Any) -> Any:
            self.was_used = True
            n = len(inputs)
            trial_fn = self.random_path
            trial_args = (n, inputs, output, size_dict)
            return trial_fn, trial_args

    eq, shapes = rand_equation(5, 3, seed=42, d_max=3)
    views = list(map(np.ones, shapes))

    exp = oe.contract(eq, *views, optimize=False)

    optimizer = NaiveRandomOptimizer(max_repeats=16)
    out = oe.contract(eq, *views, optimize=optimizer)
    assert exp == out
    assert optimizer.was_used

    assert len(optimizer.costs) == 16


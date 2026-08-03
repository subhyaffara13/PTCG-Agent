from typing import Any, Tuple

def test_contract_with_assumed_shapes(expression: str, operands: Tuple[Any]) -> None:
    """Test that we can contract with assumed shapes, and that the output is correct. This is required as we need to infer intermediate shape sizes."""

    benchmark = np.einsum(expression, *operands)
    result = contract(expression, *operands, optimize=True)
    assert np.allclose(benchmark, result)


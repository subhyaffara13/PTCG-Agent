from typing import Any

def assert_contract_order(func: Any, test_data: Any, max_size: int, benchmark: PathType) -> None:
    test_output = func(test_data[0], test_data[1], test_data[2], max_size)
    assert check_path(test_output, benchmark)


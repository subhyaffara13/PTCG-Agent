from typing import Any

def get_direct_param_fixture_func(request: FixtureRequest) -> Any:
    return request.param


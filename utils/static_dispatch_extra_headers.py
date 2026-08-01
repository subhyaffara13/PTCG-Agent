
def static_dispatch_extra_headers(backends: list[BackendIndex]) -> list[str]:
    return [
        f"#include <ATen/{dispatch_key}Functions.h>"
        for dispatch_key in static_dispatch_keys(backends)
    ]


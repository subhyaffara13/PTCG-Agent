
def require_deterministic_for_xpu(test_case):
    @wraps(test_case)
    def wrapper(*args, **kwargs):
        if is_torch_xpu_available():
            original_state = torch.are_deterministic_algorithms_enabled()
            try:
                torch.use_deterministic_algorithms(True)
                return test_case(*args, **kwargs)
            finally:
                torch.use_deterministic_algorithms(original_state)
        else:
            return test_case(*args, **kwargs)

    return wrapper


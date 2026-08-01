
def is_pytest_order_available() -> bool:
    return is_pytest_available() and _is_package_available("pytest_order")[0]


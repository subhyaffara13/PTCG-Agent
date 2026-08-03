from typing import Any

def patch_test_members(updates: dict[str, Any]):
    def decorator(test_func):
        @wraps(test_func)
        def wrapper(self, *args, **kwargs):
            # Store the original values of the specified members
            original_values = {member: getattr(self, member) for member in updates}

            # Update the members before running the subtest
            for member, value in updates.items():
                setattr(self, member, value)

            # Run the test function, allowing subtests to run
            try:
                return test_func(self, *args, **kwargs)
            finally:
                # Restore the original values of the specified members after the subtest finishes
                for member, original_value in original_values.items():
                    setattr(self, member, original_value)

        return wrapper
    return decorator


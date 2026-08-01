
def _patch_with_call_info(module_or_class, attr_name, _parse_call_info_func, target_args):
    """
    Patch a callerable `attr_name` of a module or class `module_or_class`.

    This will allow us to collect the call information, e.g. the argument names and values, also the literal expressions
    passed as the arguments.
    """
    orig_method = getattr(module_or_class, attr_name)
    if not callable(orig_method):
        return

    def patched(*args, **kwargs):
        # If the target callable is not called within a test, simply call it without modification.
        if not os.environ.get("PYTEST_CURRENT_TEST", ""):
            return orig_method(*args, **kwargs)

        try:
            orig_method(*args, **kwargs)
        except AssertionError as e:
            captured_exception = e
            # captured_traceback = e.__traceback__
            (
                full_test_name,
                test_file,
                test_lineno,
                test_obj,
                test_method,
                test_frame,
                test_traceback,
                test_code_context,
                caller_path,
                caller_lineno,
                caller_code_context,
                test_info,
            ) = _get_test_info()
            test_info = f"{test_info}\n\n{'-' * 80}\n\npatched method: {orig_method.__module__}.{orig_method.__name__}"
            call_argument_expressions = _get_call_arguments(caller_code_context)

            # This is specific
            info = _parse_call_info_func(orig_method, args, kwargs, call_argument_expressions, target_args)
            info = _prepare_debugging_info(test_info, info)

            # If the test is running in a CI environment (e.g. not a manual run), let's raise and fail the test, so it
            # behaves as usual.
            # On Github Actions or CircleCI, this is set automatically.
            # When running manually, it's the user to determine if to set it.
            # This is to avoid the patched function being called `with self.assertRaises(AssertionError):` and fails
            # because of the missing expected `AssertionError`.
            # TODO (ydshieh): If there is way to raise only when we are inside such context managers?
            # TODO (ydshieh): How not to record the failure if it happens inside `self.assertRaises(AssertionError)`?
            if os.getenv("CI") == "true":
                raise captured_exception.with_traceback(test_traceback)

            # Save this, so we can raise at the end of the current test
            captured_failure = {
                "result": "failed",
                "exception": captured_exception,
                "traceback": test_traceback,
                "info": info,
            }

            # Record the failure status and its information, so we can raise it later.
            # We are modifying the (unbound) function at class level: not its logic but only adding a new extra
            # attribute.
            if getattr(test_method.__func__, "captured_failures", None) is None:
                test_method.__func__.captured_failures = {}
            if id(test_method) not in test_method.__func__.captured_failures:
                test_method.__func__.captured_failures[id(test_method)] = []
            test_method.__func__.captured_failures[id(test_method)].append(captured_failure)

            # This modifies the `tearDown` which will be called after every tests, but we reset it back inside
            # `_patched_tearDown`.
            if not hasattr(type(test_obj).tearDown, "orig_tearDown"):
                orig_tearDown = type(test_obj).tearDown
                _patched_tearDown.orig_tearDown = orig_tearDown
                type(test_obj).tearDown = _patched_tearDown

    setattr(module_or_class, attr_name, patched)


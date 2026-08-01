
def import_transformers_or_skip():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                from transformers import AutoModelForMaskedLM, BertConfig  # noqa: F401

                return func(*args, **kwargs)
            except ImportError:
                sys.exit(TEST_SKIPS["importerror"].exit_code)

        return wrapper

    return decorator


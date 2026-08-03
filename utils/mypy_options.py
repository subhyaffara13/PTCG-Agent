import os

def mypy_options(stubgen_options: Options) -> MypyOptions:
    """Generate mypy options using the flag passed by user."""
    options = MypyOptions()
    options.follow_imports = "skip"
    options.incremental = False
    options.ignore_errors = True
    options.semantic_analysis_only = True
    options.python_version = stubgen_options.pyversion
    options.show_traceback = True
    options.transform_source = remove_misplaced_type_comments
    options.preserve_asts = True
    options.include_docstrings = stubgen_options.include_docstrings

    # Override cache_dir if provided in the environment
    environ_cache_dir = os.getenv("MYPY_CACHE_DIR", "")
    if environ_cache_dir.strip():
        options.cache_dir = environ_cache_dir
    options.cache_dir = os.path.expanduser(options.cache_dir)

    return options


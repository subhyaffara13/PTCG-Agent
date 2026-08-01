
def scoped_load_inline(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        def load_inline(*args, **kwargs):
            if IS_WINDOWS:
                # TODO(xmfan): even using TemporaryDirectoryName will result in permission error
                return cpp_extension.load_inline(*args, **kwargs)

            if "build_directory" in kwargs:
                raise AssertionError("build_directory should not be specified when using scoped_load_inline")
            with TemporaryDirectoryName() as temp_dir_name:
                if kwargs.get("verbose", False):
                    print(f'Using temporary extension directory {temp_dir_name}...', file=sys.stderr)
                kwargs["build_directory"] = temp_dir_name
                return cpp_extension.load_inline(*args, **kwargs)

        return func(*args, load_inline=load_inline, **kwargs)
    return wrapper


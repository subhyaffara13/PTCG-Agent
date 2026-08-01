
def get_last_callable(raw: str, fallback: Callable | None = None, path: str | None = None) -> Callable:
    orig_out = sys.stdout
    buffer = StringIO()
    sys.stdout = buffer

    try:
        path_str = path if path is not None else "<string>"
        code_object = compile(raw, path_str, "exec")
        env = {}

        # append exec_dir so that way python agents can import other files
        if path is not None:
            exec_dir = os.path.dirname(path)
            sys.path.append(exec_dir)
        else:
            exec_dir = None

        exec(code_object, env)
        if exec_dir is not None:
            sys.path.pop()
        sys.stdout = orig_out
        output = buffer.getvalue()
        if output:
            print(output)
        return [v for v in env.values() if callable(v)][-1]
    except Exception as e:
        sys.stdout = orig_out
        output = buffer.getvalue()
        if output:
            print(output)
        if fallback is not None:
            return fallback
        raise InvalidArgument("Invalid raw Python: " + repr(e))


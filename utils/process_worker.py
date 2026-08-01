
def process_worker() -> None:
    # Redirect standard streams to os.devnull so that user code won't interfere with the
    # parent-worker communication
    stdin = sys.stdin
    stdout = sys.stdout
    sys.stdin = open(os.devnull)
    sys.stdout = open(os.devnull, "w")

    stdout.buffer.write(b"READY\n")
    while True:
        retval = exception = None
        try:
            command, *args = pickle.load(stdin.buffer)
        except EOFError:
            return
        except BaseException as exc:
            exception = exc
        else:
            if command == "run":
                func, args = args
                try:
                    retval = func(*args)
                except BaseException as exc:
                    exception = exc
            elif command == "init":
                main_module_path: str | None
                sys.path, main_module_path = args
                del sys.modules["__main__"]
                if main_module_path and os.path.isfile(main_module_path):
                    # Load the parent's main module but as __mp_main__ instead of
                    # __main__ (like multiprocessing does) to avoid infinite recursion
                    try:
                        main = ModuleType("__mp_main__")
                        main_content = runpy.run_path(
                            main_module_path, run_name="__mp_main__"
                        )
                        main.__dict__.update(main_content)
                        sys.modules["__main__"] = sys.modules["__mp_main__"] = main
                    except BaseException as exc:
                        exception = exc
        try:
            if exception is not None:
                status = b"EXCEPTION"
                pickled = pickle.dumps(exception, pickle.HIGHEST_PROTOCOL)
            else:
                status = b"RETURN"
                pickled = pickle.dumps(retval, pickle.HIGHEST_PROTOCOL)
        except BaseException as exc:
            exception = exc
            status = b"EXCEPTION"
            pickled = pickle.dumps(exc, pickle.HIGHEST_PROTOCOL)

        stdout.buffer.write(b"%s %d\n" % (status, len(pickled)))
        stdout.buffer.write(pickled)

        # Respect SIGTERM
        if isinstance(exception, SystemExit):
            raise exception


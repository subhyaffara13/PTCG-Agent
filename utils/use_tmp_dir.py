
def use_tmp_dir(mod_name: str) -> Iterator[str]:
    current = os.getcwd()
    current_syspath = sys.path.copy()
    with tempfile.TemporaryDirectory() as tmp:
        try:
            os.chdir(tmp)
            if sys.path[0] != tmp:
                sys.path.insert(0, tmp)
            yield tmp
        finally:
            sys.path = current_syspath.copy()
            if mod_name in sys.modules:
                del sys.modules[mod_name]

            os.chdir(current)


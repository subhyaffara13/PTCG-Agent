
def test_load_module_asdict():
    with TestNamespace():
        session_buffer = BytesIO()
        dill.dump_module(session_buffer)

        global empty, names, x, y
        x = y = 0  # change x and create y
        del empty
        globals_state = globals().copy()

        session_buffer.seek(0)
        main_vars = dill.load_module_asdict(session_buffer)

        assert main_vars is not globals()
        assert globals() == globals_state

        assert main_vars['__name__'] == '__main__'
        assert main_vars['names'] == names
        assert main_vars['names'] is not names
        assert main_vars['x'] != x
        assert 'y' not in main_vars
        assert 'empty' in main_vars


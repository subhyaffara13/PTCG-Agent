
def test_session_other():
    """test dump/load_module() for a module other than __main__"""
    import test_classdef as module
    atexit.register(_clean_up_cache, module)
    module.selfref = module
    dict_objects = [obj for obj in module.__dict__.keys() if not obj.startswith('__')]

    session_buffer = BytesIO()
    dill.dump_module(session_buffer, module)

    for obj in dict_objects:
        del module.__dict__[obj]

    session_buffer.seek(0)
    dill.load_module(session_buffer, module)

    assert all(obj in module.__dict__ for obj in dict_objects)
    assert module.selfref is module


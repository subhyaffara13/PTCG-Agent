import os
import sys
import contextlib

class DummyStream:
    def write(self, text): pass
    def flush(self): pass

@contextlib.contextmanager
def silence_kaggle_warnings():
    import builtins
    orig_print = builtins.print
    def dummy_print(*args, **kwargs):
        if args and isinstance(args[0], str) and ("Loading environment" in args[0] and "failed" in args[0]):
            return
        orig_print(*args, **kwargs)
    builtins.print = dummy_print
    
    saved_pyspiel = sys.modules.get('pyspiel')
    sys.modules['pyspiel'] = None  # type: ignore
    
    dummy_stream = DummyStream()
    try:
        with contextlib.redirect_stderr(dummy_stream), contextlib.redirect_stdout(dummy_stream):
            yield
    finally:
        builtins.print = orig_print
        if saved_pyspiel is not None:
            sys.modules['pyspiel'] = saved_pyspiel
        else:
            sys.modules.pop('pyspiel', None)


def _function2():
    try: raise
    except Exception:
        from sys import exc_info
        e, er, tb = exc_info()
        return er, tb


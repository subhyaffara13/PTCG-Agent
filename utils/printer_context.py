
def printer_context(printer, **kwargs):
    original = printer._context.copy()
    try:
        printer._context.update(kwargs)
        yield
    finally:
        printer._context = original


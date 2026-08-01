
def tensorflow_code(expr, **settings):
    printer = TensorflowPrinter(settings)
    return printer.doprint(expr)


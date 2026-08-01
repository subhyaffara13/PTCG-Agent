
def classify_diop(eq, _dict=True):
    # docstring supplied externally

    matched = False
    diop_type = None
    for diop_class in all_diop_classes:
        diop_type = diop_class(eq)
        if diop_type.matches():
            matched = True
            break

    if matched:
        return diop_type.free_symbols, dict(diop_type.coeff) if _dict else diop_type.coeff, diop_type.name

    # new diop type instructions
    # --------------------------
    # if this error raises and the equation *can* be classified,
    #  * it should be identified in the if-block above
    #  * the type should be added to the diop_known
    # if a solver can be written for it,
    #  * a dedicated handler should be written (e.g. diop_linear)
    #  * it should be passed to that handler in diop_solve
    raise NotImplementedError(filldedent('''
        This equation is not yet recognized or else has not been
        simplified sufficiently to put it in a form recognized by
        diop_classify().'''))



def check_minsize(context: AHContext, minsize: int) -> bool:
    return (
        context.get_value("m") >= minsize
        and context.get_value("k") >= minsize
        and context.get_value("n") >= minsize
    )


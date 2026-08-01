
def type_iloc_constructor(context):
    def typer(obj):
        if isinstance(obj, SeriesType):
            return IlocType(obj)

    return typer


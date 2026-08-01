
def transform_try_except_stmt(builder: IRBuilder, t: TryStmt) -> None:
    def body() -> None:
        builder.accept(t.body)

    # Work around scoping woes
    def make_handler(body: Block) -> GenFunc:
        return lambda: builder.accept(body)

    def make_entry(type: Expression) -> tuple[ValueGenFunc, int]:
        return (lambda: builder.accept(type), type.line)

    handlers = [
        (make_entry(type) if type else None, var, make_handler(body))
        for type, var, body in zip(t.types, t.vars, t.handlers)
    ]

    _else_body = t.else_body
    else_body = (lambda: builder.accept(_else_body)) if _else_body else None
    transform_try_except(builder, body, handlers, else_body, t.line)


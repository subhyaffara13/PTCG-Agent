
def transform_with_stmt(builder: IRBuilder, o: WithStmt) -> None:
    # Generate separate logic for each expr in it, left to right
    def generate(i: int) -> None:
        if i >= len(o.expr):
            builder.accept(o.body)
        else:
            transform_with(
                builder, o.expr[i], o.target[i], lambda: generate(i + 1), o.is_async, o.line
            )

    generate(0)


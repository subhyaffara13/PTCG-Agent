
def _make_unop(
    op: str,
) -> t.Callable[["CodeGenerator", nodes.UnaryExpr, "Frame"], None]:
    @optimizeconst
    def visitor(self: "CodeGenerator", node: nodes.UnaryExpr, frame: Frame) -> None:
        if (
            self.environment.sandboxed and op in self.environment.intercepted_unops  # type: ignore
        ):
            self.write(f"environment.call_unop(context, {op!r}, ")
            self.visit(node.node, frame)
        else:
            self.write("(" + op)
            self.visit(node.node, frame)

        self.write(")")

    return visitor


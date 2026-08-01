
def _make_binop(op: str) -> t.Callable[["CodeGenerator", nodes.BinExpr, "Frame"], None]:
    @optimizeconst
    def visitor(self: "CodeGenerator", node: nodes.BinExpr, frame: Frame) -> None:
        if (
            self.environment.sandboxed and op in self.environment.intercepted_binops  # type: ignore
        ):
            self.write(f"environment.call_binop(context, {op!r}, ")
            self.visit(node.left, frame)
            self.write(", ")
            self.visit(node.right, frame)
        else:
            self.write("(")
            self.visit(node.left, frame)
            self.write(f" {op} ")
            self.visit(node.right, frame)

        self.write(")")

    return visitor



def optimizeconst(f: F) -> F:
    def new_func(
        self: "CodeGenerator", node: nodes.Expr, frame: "Frame", **kwargs: t.Any
    ) -> t.Any:
        # Only optimize if the frame is not volatile
        if self.optimizer is not None and not frame.eval_ctx.volatile:
            new_node = self.optimizer.visit(node, frame.eval_ctx)

            if new_node != node:
                return self.visit(new_node, frame)

        return f(self, node, frame, **kwargs)

    return update_wrapper(new_func, f)  # type: ignore[return-value]


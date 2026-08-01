
def format_tensor_computation_trace(value: VariableTracker, max_lines: int = 20) -> str:
    """Walk the FX graph backwards from a TensorVariable to show how it was
    computed, with user source locations. Graph inputs (placeholders) are always
    shown first, followed by operations in dataflow order ending at the branch
    condition."""
    if not isinstance(value, TensorVariable):
        return ""
    try:
        node = value.proxy.node

        # Collect operations and placeholders separately so placeholders (root
        # cause) always appear first regardless of traversal order.
        op_blocks: list[list[str]] = []
        placeholder_blocks: list[list[str]] = []
        visited: set[str] = set()

        def fmt_arg(a: object) -> str:
            return a.name if isinstance(a, torch.fx.Node) else repr(a)

        def walk(n: torch.fx.Node) -> None:
            if n.name in visited:
                return
            visited.add(n.name)
            source = get_node_source_info(n)

            if n.op == "placeholder":
                block = []
                if source:
                    block.append(f"# {source}")
                block.append(f"{n.name}: graph input ({n.target})")
                placeholder_blocks.append(block)
                return

            if n.op == "call_function" and len(op_blocks) < max_lines:
                target_name = getattr(n.target, "__name__", str(n.target))
                args_str = ", ".join(fmt_arg(a) for a in n.args)
                block = []
                if source:
                    block.append(f"# {source}")
                block.append(f"{n.name} = {target_name}({args_str})")
                op_blocks.append(block)

                for a in n.args:
                    if isinstance(a, torch.fx.Node):
                        walk(a)

        walk(node)

        if not op_blocks and not placeholder_blocks:
            return ""

        # Placeholders first (root cause), then ops in dataflow order (reversed
        # from the DFS collection order) ending at the branch condition.
        all_lines: list[str] = []
        for block in placeholder_blocks + list(reversed(op_blocks)):
            all_lines.extend(block)
            all_lines.append("")

        return (
            "\n\n  The branch condition involves a tensor computed as follows:\n"
            + "\n".join(f"    {line}" for line in all_lines)
        )
    except Exception:
        log.debug("format_tensor_computation_trace failed", exc_info=True)
        return ""


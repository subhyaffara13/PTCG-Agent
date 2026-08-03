from typing import Callable

def _register_logging_hooks_on_whole_graph(
    t_outputs: Sequence[torch.Tensor | GradientEdge],
) -> Callable[[], None]:
    grad_fns = list(map(_get_grad_fn_or_grad_acc, t_outputs))

    def iter_graph(roots: list[Node]) -> Iterator[Node]:
        if not roots:
            return
        seen: set[Node] = set()
        q: deque[Node] = deque()
        for node in roots:
            if node is not None:
                seen.add(node)
                q.append(node)

        while q:
            node = q.popleft()
            for fn, _ in node.next_functions:
                if fn in seen or fn is None:
                    continue
                seen.add(fn)
                q.append(fn)

            yield node

    def fmt(t: torch.Tensor | None) -> str:
        # Avoid circular import
        from torch.utils._dtype_abbrs import dtype_abbrs

        if t is None:
            return "None"
        return f"{dtype_abbrs[t.dtype]}[{', '.join(map(str, t.shape))}]"

    def prehook(grad_outputs: Sequence[torch.Tensor | None]) -> None:
        node = torch._C._current_autograd_node()
        grad_outputs_str = f"[{','.join(fmt(t) for t in grad_outputs)}]"
        log_str = f"Executing: {node} with grad_outputs: {grad_outputs_str}"
        log.debug(log_str)

    handles = [node.register_prehook(prehook) for node in iter_graph(grad_fns)]

    def unregister_hooks() -> None:
        for handle in handles:
            handle.remove()

    return unregister_hooks


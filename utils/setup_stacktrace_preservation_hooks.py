from typing import Any, Callable

def setup_stacktrace_preservation_hooks(roots: list[torch.autograd.graph.Node]) -> None:
    def iter_graph(
        roots: list[torch.autograd.graph.Node],
    ) -> Iterator[torch.autograd.graph.Node]:
        if not roots:
            return
        seen = set()
        q = collections.deque()
        for node in roots:
            if node is not None and node not in seen:
                seen.add(node)
                q.append(node)

        while q:
            node = q.popleft()
            for fn, _idx in node.next_functions:
                if fn in seen or fn is None:
                    continue
                seen.add(fn)
                q.append(fn)

            yield node

    def get_callback(saved_stack_: list[str]) -> Callable[[], None]:
        def callback() -> None:
            global callback_set
            fx_traceback.set_stack_trace(saved_stack_)
            callback_set = False

        return callback

    def get_prehook(stack_: list[str], seq_nr: int) -> Callable[[Any], None]:
        def prehook(grad_output: Any) -> None:
            global callback_set

            if not callback_set:
                torch.autograd.variable.Variable._execution_engine.queue_callback(  # type: ignore[attr-defined]
                    get_callback(fx_traceback.format_stack())
                )
                callback_set = True

            fx_traceback.set_stack_trace(stack_)
            fx_traceback.set_grad_fn_seq_nr(seq_nr)
            fx_traceback._mark_autograd_backward()

        return prehook

    def get_posthook(
        special_stack_: list[str], seq_nr: int
    ) -> Callable[[Any, Any], None]:
        def posthook(grad_input: Any, grad_output: Any) -> None:
            fx_traceback.set_stack_trace(special_stack_)
            fx_traceback.reset_grad_fn_seq_nr()
            fx_traceback._reset_autograd_backward()

        return posthook

    for node in iter_graph(roots):
        # pyrefly: ignore[missing-attribute]
        forward_node_stack = node.metadata.get("traceback_", [])
        node.register_prehook(get_prehook(forward_node_stack, node._sequence_nr()))

        special_stack = forward_node_stack.copy()
        special_stack.append(fx_traceback.GRADIENT_ACC_SPECIAL_STACK)
        node.register_hook(get_posthook(special_stack, node._sequence_nr()))


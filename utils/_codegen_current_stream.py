
def _codegen_current_stream(device: torch.device, cg: "PyCodegen") -> None:
    cg.add_push_null(
        lambda: cg.load_import_from(
            torch._dynamo.graph_bytecode_inputs.__name__,  # type: ignore[implicit-imports]
            "stash_graph_created_object",
        )
    )
    cg(CurrentStreamSource(device))
    cg.extend_output(create_call_function(1, False))


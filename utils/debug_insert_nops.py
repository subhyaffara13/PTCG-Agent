
def debug_insert_nops(
    frame: DynamoFrameType, cache_size: int, hooks: Any, _: Any, *, skip: int = 0
) -> ConvertFrameReturn:
    """used to debug jump updates"""

    def insert_nops(instructions: list[Any], code_options: Any) -> None:
        instructions.insert(0, create_instruction("NOP"))
        instructions.insert(0, create_instruction("NOP"))

    metrics_context = torch._dynamo.utils.get_metrics_context()
    with torch._dynamo.utils.dynamo_timed("debug_insert_nops"), metrics_context:
        if is_generator(frame.f_code):
            return ConvertFrameReturn()

        debug_checks(frame.f_code)
        code, _ = transform_code_object(frame.f_code, insert_nops)
        graph = OutputGraph(
            code_options={},
            compiler_fn=None,
            root_tx=None,  # type: ignore[arg-type]
            export=False,
            export_constraints=[],
            frame_state={"_id": 0},
            # TODO: shouldn't this be f_locals/f_globals from frame?
            local_scope=locals(),
            global_scope=globals(),
            f_code=frame.f_code,
            torch_function_mode_stack=[],
            package=None,
        )

        return wrap_guarded_code(
            GuardedCode(
                code,
                CheckFunctionManager(frame.f_code, graph).guard_manager,  # type: ignore[arg-type]
                CompileId(frame_id=0, frame_compile_id=0),
            )
        )



def trace_frame(
    code: types.CodeType,
    globals: dict[str, object],
    locals: dict[str, object],
    builtins: dict[str, object],
    closure: tuple[CellType],
    compiler_fn: CompilerFn,
    tf_mode_stack: list[torch.overrides.TorchFunctionMode],
    one_graph: bool,
    speculation_log: SpeculationLog,
    instructions: list[Instruction],
    code_options: dict[str, object],
    *,
    export: bool = False,
    export_constraints: Any | None = None,
    frame_state: dict[str, int | FrameStateSizeEntry] | None = None,
    distributed_state: DistributedState | None = None,
    package: CompilePackage | None = None,
) -> DynamoTracerOutput:
    from torch.fx.experimental.validator import bisect, translation_validation_enabled

    speculation_log.restart()  # type: ignore[has-type]
    exn_vt_stack = ExceptionStack()
    tracer = InstructionTranslator(
        instructions,
        code,
        locals,
        globals,
        builtins,
        closure,
        tf_mode_stack,
        code_options,
        compiler_fn,
        one_graph,
        export,
        export_constraints,
        frame_state=frame_state,
        speculation_log=speculation_log,  # type: ignore[has-type]
        exn_vt_stack=exn_vt_stack,
        distributed_state=distributed_state,  # type: ignore[has-type]
        package=package,
    )

    def run_tracer() -> None:
        try:
            tracer.output.mark_bytecode_tracing_start()
            with tracing(tracer.output.tracing_context), tracer.set_current_tx():
                tracer.run()
        except exc.UnspecializeRestartAnalysis:
            speculation_log.clear()  # type: ignore[has-type]
            raise
        except (
            exc.SpeculationRestartAnalysis,
            exc.TensorifyScalarRestartAnalysis,
            exc.SkipFrame,
        ):
            raise
        except Exception:
            if translation_validation_enabled():
                bisect(tracer.output.shape_env)
            raise
        finally:
            tracer.output.call_cleanup_hooks()
            tracer.f_locals = {}

    try:
        run_tracer()
        tracer_output = DynamoTracerOutput(tracer)
        output = tracer_output.output_graph
        assert output is not None
        assert output.output_instructions
        instructions[:] = output.output_instructions
        code_options.update(output.code_options)
        propagate_inst_exn_table_entries(instructions)
        check_inst_exn_tab_entries_valid(instructions)
        instructions[:] = remove_pointless_jumps(remove_dead_code(instructions))
    except Exception as e:
        e._torch_dynamo_tracer_output = DynamoTracerOutput(tracer, error=True)  # type: ignore[attr-defined]
        raise
    return tracer_output


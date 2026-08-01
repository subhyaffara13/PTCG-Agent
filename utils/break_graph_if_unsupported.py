
def break_graph_if_unsupported(
    *, push: bool, msg_prefix: str
) -> Callable[
    [Callable[..., None]], Callable[[InstructionTranslatorBase, Instruction], None]
]:
    def decorator(
        inner_fn: Callable[..., None],
    ) -> Callable[[InstructionTranslatorBase, Instruction], None]:
        @functools.wraps(inner_fn)
        def wrapper(self: InstructionTranslatorBase, inst: Instruction) -> None:
            prev_push = self.current_instruction_push
            self.current_instruction_push = push
            speculation = self.speculate()
            if speculation.failed(self):
                # no need to restore current_instruction_push if speculation failed
                assert speculation.reason is not None
                return handle_graph_break(self, inst, speculation.reason)
            try:
                return inner_fn(self, inst)
            except (Unsupported, UserError) as excp:
                if self.active_generic_context_managers:
                    # raise original graph break if fullgraph/error_on_graph_break=True
                    if self.one_graph or self.error_on_graph_break:
                        raise

                    # We don't support graph break under GenericContextWrappingVariable,
                    # If there is, we roll back to the checkpoint and fall back.
                    if isinstance(excp, Unsupported):
                        excp.remove_from_stats()
                    unimplemented(
                        gb_type="Graph break under GenericContextWrappingVariable",
                        context=f"Active generic context managers: {self.active_generic_context_managers}",
                        explanation="Attempted to graph break in an active context manager(s) that doesn't support graph breaking.",
                        hints=[
                            "Move the offending context manager(s) to outside the compiled region.",
                            *graph_break_hints.CAUSED_BY_EARLIER_GRAPH_BREAK,
                        ],
                        from_exc=excp,
                    )

                if getattr(excp, "skip_frame", False):
                    raise

                if not self.should_compile_partial_graph():
                    raise

                if self.maybe_has_backedge():
                    self.raise_loop_graph_break(self.f_code, excp)

                self.log_graph_break(
                    self.code_options,
                    reason=f"{msg_prefix}:\n\n{str(excp)}",
                    exc=excp,
                )

                if isinstance(excp, Unsupported):
                    excp.remove_from_stats()
                    excp.add_to_stats("graph_break")
                speculation.reason = GraphCompileReason(
                    getattr(excp, "msg", str(excp)),
                    getattr(excp, "real_stack", [self.frame_summary()]),
                )
            finally:
                self.current_instruction_push = prev_push
            speculation.fail_and_restart_analysis(self.error_on_graph_break)

        def handle_graph_break(
            self: InstructionTranslatorBase,
            inst: Instruction,
            reason: GraphCompileReason,
        ) -> None:
            if (
                sys.version_info >= (3, 11)
                and sys.version_info < (3, 12)
                and inst.opname == "CALL"
            ):
                # stack effect for PRECALL + CALL is split between the two instructions
                stack_effect = dis.stack_effect(
                    dis.opmap["PRECALL"], inst.arg
                ) + dis.stack_effect(dis.opmap["CALL"], inst.arg)
            else:
                stack_effect = dis.stack_effect(inst.opcode, inst.arg)

            log.debug("%s triggered compile", inst.opname)
            all_stack_locals_metadata = self.output.compile_subgraph(
                self, reason=reason, stack_pops=int(push) - stack_effect
            )
            cg = PyCodegen(self.output.root_tx)
            cleanup: list[Instruction] = []
            _reconstruct_block_stack(self, cg, cleanup)
            self.output.add_output_instructions(cg.get_instructions())
            del cg

            if sys.version_info >= (3, 11) and inst.opname == "CALL":
                kw_names = (
                    self.kw_names.as_python_constant()
                    if self.kw_names is not None
                    else ()
                )
                if len(kw_names) > 0:
                    # KW_NAMES no longer used in 3.13
                    assert sys.version_info < (3, 13)
                    self.output.add_output_instructions(
                        [create_instruction("KW_NAMES", argval=kw_names)]
                    )
                assert inst.arg is not None
                call_insts = create_call_function(inst.arg, False)
                call_insts[-1].copy_positions(inst)
                self.output.add_output_instructions(call_insts)
            else:
                # copy instruction, but without exception table data
                assert inst.target is None
                inst_copy = copy.copy(inst)
                inst_copy.exn_tab_entry = None
                self.output.add_output_instructions([inst_copy])

            self.output.add_output_instructions(cleanup)

            self.popn(int(push) - stack_effect)
            if push:
                self.push(UnknownVariable())
            self.output.add_output_instructions(
                self.create_call_resume_at(
                    self.next_instruction,
                    all_stack_locals_metadata,
                )
            )

        return wrapper

    return decorator


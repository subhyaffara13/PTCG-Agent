
def unlift_tokens(
    fw_module: torch.fx.GraphModule,
    fw_metadata: "ViewAndMutationMeta",
    aot_config: "AOTConfig",
    bw_module: torch.fx.GraphModule | None = None,
) -> None:
    # Remove the tokens from the inputs/outputs of the graph since inductor does
    # not want these extra inputs/outputs, and replace them with
    # _make_token() to create a token, and _sink_tokens() to collect the
    # tokens.  See Note [Side-Effectful Tokens in AOTAutograd]
    # Logic:
    # 1. In the case of with_effects:
    #   Before:
    #   ```
    #   def forward(self, token, arg1_1):
    #       with_effects = torch.ops.higher_order.with_effects(token, ...)
    #       getitem = with_effects[0]
    #       getitem_1 = with_effects[0]
    #       return (getitem, getitem_1)
    #   ```
    #
    #   After:
    #   ```
    #   def forward(self, arg1_1):
    #       _make_token_default = torch.ops.prims._make_token.default()
    #       with_effects = torch.ops.higher_order.with_effects(_make_token_default, ...)
    #       getitem = with_effects[0]
    #       getitem_1 = with_effects[0]
    #       _sink_tokens_default = torch.ops.prims._sink_tokens.default([getitem]);
    #       return (getitem_1,)
    #   ```
    #
    # 2. In the case of an invoke_subgraph node, we will use the
    # InvokeSubgraphCache to determine if the subgraph has effects. Then we will
    # turn it into a `with_effects` node. This is so that at the toplevel graph,
    # the nodes will have the correct with_effects threading. We will apply this
    # pass recursively to submodules so the tokens will be removed from the
    # subgraph's inputs.
    #
    #   Before:
    #   ```
    #   def forward(self, token, arg1_1):
    #       repeated_subgraph0 = self.repeated_subgraph0
    #       invoke_subgraph = torch.ops.higher_order.invoke_subgraph(
    #           repeated_subgraph0, 'subgraph_0', token, x, arg1_1)
    #       getitem = invoke_subgraph[0]
    #       getitem_1 = invoke_subgraph[1]
    #       return (getitem, getitem1)
    #   ```
    #
    #   After:
    #   ```
    #   def forward(self, arg1_1):
    #       _make_token_default = torch.ops.prims._make_token.default()
    #       repeated_subgraph0 = self.repeated_subgraph0
    #       with_effects_1 = torch.ops.higher_order.with_effects(
    #           _make_token_default, torch.ops.higher_order.invoke_subgraph,
    #           repeated_subgraph0, 'subgraph_0', arg1_1)
    #       getitem = with_effects_1[0]
    #       getitem_1 = with_effects_1[1];  with_effects_1 = None
    #       _sink_tokens_default = torch.ops.prims._sink_tokens.default([getitem])
    #       return (getitem_1,)
    #   ```
    #
    # 3. The toplevel module should have the following invariants:
    #   forward:
    #     expected_num_erased_inputs == len(fw_metadata.tokens)
    #     expected_num_erased_outputs == len(fw_metadata.tokens)
    #   backward:
    #     expected_num_erased_inputs == fw_metadata.num_backward_tokens
    #     expected_num_erased_outputs == fw_metadata.num_backward_tokens
    num_forward_tokens = len(fw_metadata.tokens)
    num_backward_tokens = fw_metadata.num_backward_tokens

    def replace_input_token_with_make_token(
        module: torch.fx.GraphModule, node: torch.fx.Node
    ) -> None:
        with module.graph.inserting_before(node):
            new_token_node = module.graph.call_function(
                torch.ops.prims._make_token.default, ()
            )
            new_token_node.meta["val"] = torch.tensor([])
            new_token_node.meta["tensor_meta"] = torch.tensor([])
            node.replace_all_uses_with(new_token_node)
            module.graph.erase_node(node)

    def get_output_tokens(node: torch.fx.Node) -> set[torch.fx.Node]:
        output_tokens = set()
        for user in list(node.users.keys()):
            # Check if this is a getitem accessing index 0 (the token)
            if (
                user.op == "call_function"
                and user.target is operator.getitem
                and len(user.args) > 1
                and user.args[1] == 0
            ):
                # Check if this getitem is used in an output
                for user_user in list(user.users.keys()):
                    if user_user.op == "output":
                        output_tokens.add(user)
        return output_tokens

    def _unlift_tokens_from_module_helper(
        module: torch.fx.GraphModule,
        subgraph_str: str,
        expected_num_erased: int | None,
    ) -> None:
        input_token_nodes = set()
        output_token_nodes = set()

        for node in module.graph.nodes:
            if (
                node.op == "call_function"
                and node.target is torch.ops.higher_order.with_effects
            ):
                if node.args[0].op == "placeholder":
                    input_token_nodes.add(node.args[0])
                    replace_input_token_with_make_token(module, node.args[0])

                tokens_from_with_effects = get_output_tokens(node)
                output_token_nodes = output_token_nodes | tokens_from_with_effects

            elif (
                node.op == "call_function"
                and node.target is torch.ops.higher_order.invoke_subgraph
            ):
                subgraph_node, identifier, *operands = node.args

                # Check if subgraph has effects by looking in the cache
                from torch._guards import InvokeSubgraphCache, TracingContext

                effects = None
                tracing_ctx = TracingContext.try_get()
                if tracing_ctx:
                    invoke_subgraph_cache = (
                        tracing_ctx.hop_dispatch_set_cache.get_cache(
                            torch.ops.higher_order.invoke_subgraph
                        )
                    )
                    if invoke_subgraph_cache:
                        if not isinstance(invoke_subgraph_cache, InvokeSubgraphCache):
                            raise AssertionError(
                                f"expected InvokeSubgraphCache, got {type(invoke_subgraph_cache)}"
                            )
                        effects = invoke_subgraph_cache.get_effects(identifier)

                if effects is not None:
                    # Wrap invoke_subgraph with with_effects
                    # Before: invoke_subgraph(subgraph, id, token, *args) -> (token_out, result)
                    # After: with_effects(token, invoke_subgraph, subgraph, id, *args) -> (token_out, result)
                    #
                    # Note: The subgraph itself will be unlifted separately when we iterate
                    # through named_modules() below.

                    num_tokens = len(effects)
                    if num_tokens != 1:
                        raise AssertionError(
                            f"Multiple token subgraph NYI, got {num_tokens} tokens"
                        )
                    token_args = operands[:num_tokens]
                    non_token_args = operands[num_tokens:]

                    # Create with_effects wrapper around invoke_subgraph
                    # with_effects(token, op, *args) where op is invoke_subgraph
                    # Pass the subgraph and non-token args to invoke_subgraph
                    with module.graph.inserting_before(node):
                        new_node = module.graph.call_function(
                            torch.ops.higher_order.with_effects,
                            # pyrefly: ignore [bad-argument-type]
                            (
                                token_args[0],  # pyrefly: ignore[bad-argument-type]
                                torch.ops.higher_order.invoke_subgraph,
                                subgraph_node,
                                identifier,
                                *tuple(non_token_args),
                            ),
                        )
                        node.replace_all_uses_with(new_node)
                        new_node.meta = node.meta
                        module.graph.erase_node(node)

                    for token in token_args:
                        if token.op == "placeholder":
                            input_token_nodes.add(token)
                            replace_input_token_with_make_token(module, token)

                    # Get output tokens from the new with_effects node
                    tokens_from_invoke_subgraph = get_output_tokens(new_node)
                    output_token_nodes = (
                        output_token_nodes | tokens_from_invoke_subgraph
                    )

        if not output_token_nodes and not input_token_nodes:
            return

        output_node = next(reversed(module.graph.find_nodes(op="output")))
        if output_node is None:
            raise AssertionError("output node not found in graph")
        with module.graph.inserting_before(output_node):
            module.graph.call_function(
                torch.ops.prims._sink_tokens.default,
                (list(output_token_nodes),),
            )
        new_out_args = tuple(
            [out for out in output_node.args[0] if out not in output_token_nodes]
        )
        output_node.args = (new_out_args,)

        if expected_num_erased:
            if len(input_token_nodes) != expected_num_erased:
                raise AssertionError(
                    f"{subgraph_str} num_erased_inputs:{len(input_token_nodes)} "
                    f"{input_token_nodes} != expected {expected_num_erased} \n"
                    f"{fw_module.print_readable(print_output=False)}"
                )
            if len(output_token_nodes) != expected_num_erased:
                raise AssertionError(
                    f"{subgraph_str} num_erased_outs:{len(output_token_nodes)} "
                    f"{output_token_nodes} != expected {expected_num_erased} \n"
                    f"{fw_module.print_readable(print_output=False)}"
                )

        module.recompile()

    def unlift_tokens_from_module(
        module: torch.fx.GraphModule, subgraph_str: str, expected_num_erased: int
    ) -> None:
        for name, m in module.named_modules():
            if isinstance(m, torch.fx.GraphModule):
                if name == "":
                    _unlift_tokens_from_module_helper(
                        m, subgraph_str, expected_num_erased
                    )
                else:
                    # Subgraph -- we may or may not have effects applied
                    _unlift_tokens_from_module_helper(m, f"{subgraph_str}_{name}", None)

    if num_forward_tokens > 0:
        if aot_config.enable_log:
            from torch._dynamo.utils import lazy_format_graph_code

            aot_graphs_effects_log.debug(
                "%s",
                lazy_format_graph_code(
                    "Forward graph before unlifting tokens",
                    fw_module,
                    aot_config.aot_id,
                    include_stride=True,
                    include_device=True,
                    colored=True,
                ),
            )
        unlift_tokens_from_module(
            fw_module,
            "forward",
            num_forward_tokens,
        )

    if bw_module is not None and num_backward_tokens > 0:
        if aot_config.enable_log:
            from torch._dynamo.utils import lazy_format_graph_code

            aot_graphs_effects_log.debug(
                "%s",
                lazy_format_graph_code(
                    "Backward graph before unlifting tokens",
                    bw_module,
                    aot_config.aot_id,
                    include_stride=True,
                    include_device=True,
                    colored=True,
                ),
            )
        unlift_tokens_from_module(bw_module, "backward", num_backward_tokens)

    # This is sad, but we need to update the metadata to get rid of
    # the tokens.
    fw_metadata.tokens = {}
    fw_metadata.num_backward_tokens = 0


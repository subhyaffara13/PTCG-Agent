
def _insert_dequant_stubs_for_custom_module_lstm_output(
    node: Node,
    model: torch.nn.Module,
    named_modules: dict[str, torch.nn.Module],
    graph: Graph,
) -> Node:
    """
    Insert DeQuantStubs after each internal output node of custom module LSTM.

    Custom module LSTM outputs are nested tuples of the structure (output, (hidden0, hidden1)),
    Since we cannot dequantize a tuple as a whole, we must first break down the tuple into its
    components through `getitem`. This function transforms the graph as follows:

      (1) Split the LSTM node into (output, (hidden0, hidden1))
      (2) Insert a DeQuantStub after each internal node
      (3) Recombine the DeQuantStubs into the same structure as before
      (4) Reroute all consumers of the original LSTM node and its sub-nodes
          (e.g. lstm[0])

    Before:
                   lstm_output
                        |
                        v
                  original_user(s)
    After:
                   lstm_output
                  /           \\
                 /  (getitem)  \\
                /               \\
               v                 v
             output            hidden
               |               /   \\
         (DeQuantStub)        (getitem)
               |             /       \\
               v            v         v
           output_dq     hidden0    hidden1
               |            |         |
               |    (DeQuantStub) (DeQuantStub)
               |            |         |
               |            v         v
               |      hidden0_dq  hidden1_dq
               |            \\       /
               |              (tuple)
               |              \\   /
               |               v  v
               |             hidden_dq
               \\               /
                \\   (tuple)   /
                 v            v
                 lstm_output_dq
                       |
                       v
                original_user(s)

    For step (4), reroute all users of the original LSTM node(s) as follows:
      lstm_output -> lstm_output_dq
      lstm_output[0] -> output_dq
      lstm_output[1] -> hidden_dq
      lstm_output[1][0] -> hidden0_dq
      lstm_output[1][1] -> hidden1_dq

    Return the node `lstm_output_dq`.
    """
    # (1) Split the LSTM node into (output, (hidden0, hidden1))
    # (2) Insert a DeQuantStub after each internal node
    with graph.inserting_after(node):
        output = graph.call_function(operator.getitem, (node, 0))
        output_dq = _insert_dequant_stub(output, model, named_modules, graph)
    with graph.inserting_after(output_dq):
        hidden = graph.call_function(operator.getitem, (node, 1))
    with graph.inserting_after(hidden):
        hidden0 = graph.call_function(operator.getitem, (hidden, 0))
        hidden0_dq = _insert_dequant_stub(hidden0, model, named_modules, graph)
    with graph.inserting_after(hidden0_dq):
        hidden1 = graph.call_function(operator.getitem, (hidden, 1))
        hidden1_dq = _insert_dequant_stub(hidden1, model, named_modules, graph)

    # (3) Recombine the DeQuantStubs into the same structure as before
    with graph.inserting_after(hidden1_dq):
        hidden_dq = graph.call_function(tuple, ([hidden0_dq, hidden1_dq],))
    with graph.inserting_after(hidden_dq):
        lstm_output_dq = graph.call_function(tuple, ([output_dq, hidden_dq],))

    # (4) Reroute all consumers of the original LSTM node and its sub-nodes
    for user in list(node.users.keys()):
        if user != output and user != hidden:
            user.replace_input_with(node, lstm_output_dq)
    # The getitem and tuple nodes we added here may interfere with reference quantized
    # pattern matching, so we need to redirect the consumers of internal nodes to the
    # corresponding nodes with DeQuantStubs (e.g. lstm_output_dq[0] -> output_dq) attached,
    # in order to preserve reference patterns like "dequantize - consumer - quantize".
    _reroute_tuple_getitem_pattern(graph)
    return lstm_output_dq


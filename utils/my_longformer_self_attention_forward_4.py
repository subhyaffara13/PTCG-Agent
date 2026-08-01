
def my_longformer_self_attention_forward_4(
    self,
    hidden_states,
    attention_mask=None,
    is_index_masked=None,
    is_index_global_attn=None,
    is_global_attn=None,
):
    global_mask = is_index_global_attn.int()
    # The following check is based on the dummy inputs (only the first token is global).
    assert (
        len(global_mask.shape) == 2
        and global_mask.shape[0] == 1
        and global_mask.count_nonzero().item() == 1
        and global_mask.tolist()[0][0] == 1
    )

    input_mask = is_index_masked.float()
    # TODO: The filtering value may be -10000.0 or -inf. Check the huggingface implementation.
    input_mask = input_mask.masked_fill(is_index_masked, -10000.0)
    # Yet another way to generate input_mask = torch.masked_fill(attention_mask, is_index_global_attn, 0.0)

    # TODO: add postprocessing of ONNX model to calculate based on graph input: input_mask = (attention_mask - 1) * 10000.0
    # TODO: add postprocessing of ONNX model to use graph input directly: global_mask = global_attention_mask

    # The following check is based on the dummy inputs (only the last token is masked).
    assert (
        len(input_mask.shape) == 2
        and input_mask.shape[0] == 1
        and input_mask.count_nonzero().item() == 1
        and input_mask.tolist()[0][-1] == -10000.0
    )

    weight = torch.stack(
        (
            self.query.weight.transpose(0, 1),
            self.key.weight.transpose(0, 1),
            self.value.weight.transpose(0, 1),
        ),
        dim=weight_bias_format,
    )

    if weight_bias_format == 1:
        # shape is (hidden_size, 3*hidden_size) for format 1, otherwise (3, hidden_size, hidden_size) by default
        weight = weight.reshape(self.embed_dim, 3 * self.embed_dim)

    global_weight = torch.stack(
        (
            self.query_global.weight.transpose(0, 1),
            self.key_global.weight.transpose(0, 1),
            self.value_global.weight.transpose(0, 1),
        ),
        dim=weight_bias_format,
    )

    if weight_bias_format == 1:
        global_weight = global_weight.reshape(self.embed_dim, 3 * self.embed_dim)

    if weight_bias_format == 1:
        bias = torch.stack((self.query.bias, self.key.bias, self.value.bias), dim=0)
        bias = bias.reshape(3 * self.embed_dim)
        global_bias = torch.stack((self.query_global.bias, self.key_global.bias, self.value_global.bias), dim=0)
        global_bias = global_bias.reshape(3 * self.embed_dim)
    else:
        bias = torch.stack(
            (self.query.bias, self.key.bias, self.value.bias, self.key_global.bias, self.value_global.bias), dim=0
        )
        bias = bias.reshape(5 * self.embed_dim)
        global_bias = self.query_global.bias
        global_bias = global_bias.reshape(1 * self.embed_dim)

    attn_output = torch.ops.onnxruntime.LongformerAttention(
        hidden_states,
        weight,
        bias,
        input_mask,
        global_weight,
        global_bias,
        global_mask,
        self.num_heads,
        self.one_sided_attn_window_size,
    )

    assert attn_output.size() == hidden_states.size(), "Unexpected size"

    outputs = (attn_output,)
    return outputs


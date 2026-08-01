
def my_longformer_self_attention_forward_4_3_2(
    self,
    hidden_states,
    attention_mask=None,
    layer_head_mask=None,
    is_index_masked=None,
    is_index_global_attn=None,
    is_global_attn=None,
    output_attentions=False,
):
    assert output_attentions is False
    assert layer_head_mask is None
    return my_longformer_self_attention_forward_4(
        self,
        hidden_states,
        attention_mask,
        is_index_masked,
        is_index_global_attn,
        is_global_attn,
    )


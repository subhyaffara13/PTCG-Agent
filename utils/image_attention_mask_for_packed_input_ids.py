
def image_attention_mask_for_packed_input_ids(input_ids, tokenizer, return_tensors):
    if return_tensors == "pt":
        return image_attention_mask_for_packed_input_ids_pt(input_ids, tokenizer)


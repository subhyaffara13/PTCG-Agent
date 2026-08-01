
def create_attention_mask(input_ids, pad_token_id):
    attention_mask = np.ones(input_ids.shape, dtype=np.int32)
    for i in range(input_ids.shape[0]):
        abs_pos = 0
        for j in range(input_ids.shape[1]):
            if input_ids[i][j] == pad_token_id and abs_pos == 0:
                attention_mask[i][j] = 0
            else:
                abs_pos += 1
    return attention_mask


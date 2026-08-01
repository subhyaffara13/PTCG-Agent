
def get_embed_positions(embed_positions, position_ids):
    return embed_positions.to(position_ids.device).repeat(position_ids.shape[0], 1, 1)


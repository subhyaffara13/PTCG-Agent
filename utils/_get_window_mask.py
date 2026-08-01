
def _get_window_mask(T: int, S: int, local_window_size: tuple[int, int]):
  query_pos = jnp.array(range(T))
  key_pos = jnp.array(range(S))
  left_window, right_window = local_window_size
  left_mask = query_pos[..., None] <= key_pos[..., None, :] + left_window
  right_mask = query_pos[..., None] >= key_pos[..., None, :] - right_window
  return jnp.logical_and(right_mask, left_mask)[None, None, :, :]


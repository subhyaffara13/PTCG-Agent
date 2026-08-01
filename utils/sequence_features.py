
def sequence_features(
    state_features: list[str | int],
    legal_actions: list[int],
    num_distinct_actions: int,
) -> chex.Array:
  """Constructs features for each sequence by extending state features.

  Sequences features are constructed by concatenating one-hot features
  indicating each action to the information state features and stacking them.

  Args:
    state_features: The features of the information state.
    legal_actions: The list of legal actions available in the state. Determines
      the number of rows in the returned feature matrix.
    num_distinct_actions: The number of globally distinct actions in the game.
      Determines the length of the action feature vector concatenated onto the
      state features.

  Returns:
    A `chex.Array` feature matrix with one row for each sequence and # state
    features plus `num_distinct_actions`-columns.
  """
  state_features = jnp.asarray(state_features)
  state_features = jnp.repeat(
      state_features[jnp.newaxis], len(legal_actions), axis=0
  )
  action_features = jax.nn.one_hot(
      jnp.asarray(legal_actions, dtype=jnp.float32), num_distinct_actions
  )
  return jnp.concat([state_features, action_features], axis=-1)


def sequence_features(
    state_features: list[str | int],
    legal_actions: list[int],
    num_distinct_actions: int,
) -> torch.Tensor:
  """Constructs features for each sequence by extending state features.

  Sequences features are constructed by concatenating one-hot features
  indicating each action to the information state features and stacking them.

  Args:
    state_features: The features of the information state.
    legal_actions: The list of legal actions available in the state. Determines
      the number of rows in the returned feature matrix.
    num_distinct_actions: The number of globally distinct actions in the game.
      Determines the length of the action feature vector concatenated onto the
      state features.

  Returns:
    A `torch.Tensor` feature matrix with one row for each sequence and # state
    features plus `num_distinct_actions`-columns.
  """
  state_features = torch.as_tensor(state_features)
  state_features = state_features[None].repeat(len(legal_actions), 1)
  action_features = F.one_hot(
      torch.LongTensor(legal_actions), num_distinct_actions
  )
  return torch.concatenate([state_features, action_features], dim=-1)


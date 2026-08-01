
def spawn_entity(key: chex.PRNGKey, state: EnvState) -> Tuple[chex.Array, jnp.ndarray]:
    """Spawn new enemy or treasure at random location with random direction."""
    key_lr, key_gold, key_slot = jax.random.split(key, 3)
    lr = jax.random.choice(key_lr, jnp.array([1, 0]))
    is_gold = jax.random.choice(
        key_gold, jnp.array([1, 0]), p=jnp.array([1 / 3, 2 / 3])
    )
    x = (1 - lr) * 9  # l-to-r starts at 0
    # Entities are represented as 5 dimensional arrays
    # 0: Position y, 1: Slot x, 2: lr (from l to r dir), 3: Gold indicator
    # 4: whether entity is filled/not an open slot

    # Sampling problem: Need to get rid of jnp.where due to concretization
    # Sample random order of entries to go through
    # Check if element is free with while loop and stop if position is found
    # or all elements have been checked
    state_entities = state.entities[:, 4]  # Only use col 4 indicating free
    slot, free = while_sample_slots(key_slot, state_entities)
    entity = jnp.array([x, slot + 1, lr, is_gold, free])
    return entity, slot


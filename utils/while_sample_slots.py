from typing import Tuple

def while_sample_slots(
    key: chex.PRNGKey, state_entities: chex.Array
) -> Tuple[jnp.ndarray, jnp.ndarray]:
    """Go through random order of slots until slot is found that is free."""
    init_val = jnp.array([0, 0])
    # Sample random order of slot entries to go through - hack around jnp.where
    order_to_go_through = jax.random.permutation(key, jnp.arange(8))
    perm_entities = state_entities[order_to_go_through]

    def condition_to_check(val):
        # Check if we haven't gone through all possible slots and whether free
        return jnp.logical_and(val[0] < 7, val[1] == 0)

    def update(val):
        # Increase list counter - slot that has been checked
        val = val.at[0].set(val[0] + 1)
        # Check if slot is still free
        free = perm_entities[val[0]] == 0
        val = val.at[1].set(free)
        return val

    id_and_free = jax.lax.while_loop(condition_to_check, update, init_val)
    # Return slot id and whether it is free
    slot_id = order_to_go_through[id_and_free[0]]
    free_slot = id_and_free[1]
    return slot_id, free_slot


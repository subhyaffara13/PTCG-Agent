from typing import Tuple

def step_entities(
    state: EnvState,
) -> Tuple[EnvState, jnp.ndarray, bool]:
    """Update positions of the entities and return reward, done."""
    done, reward = 0, jnp.array(0)
    # Loop over entities and check for collisions - either gold or enemy
    entities = state.entities
    for i in range(8):
        x = entities[i]
        slot_filled = x[4] != 0
        # Get boolean for any collision with either gold or enemy
        coords = jnp.logical_and(x[0] == state.player_x, x[1] == state.player_y)
        collision = jnp.logical_and(coords, slot_filled)
        # If collision with gold: empty gold and give positive reward
        collision_gold = jnp.logical_and(collision, x[3])
        reward += collision_gold
        # Set row i to zeros if collision with gold
        entities = entities.at[i].set(x * (1 - collision_gold))

        # If collision with enemy: terminate the episode
        collision_enemy = jnp.logical_and(collision, 1 - x[3])
        done += collision_enemy

    # Loop over entities and move them in direction
    time_to_move = state.move_timer == 0
    move_timer = jax.lax.select(time_to_move, state.move_speed, state.move_timer)

    old_entities = entities
    for i in range(8):
        x = entities[i]
        slot_filled = x[4] != 0
        lr = x[2]
        # Update position left and right move
        x = x.at[0].set(jax.lax.select(slot_filled, x[0] + 1 * lr - 1 * (1 - lr), x[0]))

        # Update if entity moves out of the frame - reset everything to zeros
        outside_of_frame = jnp.logical_or(x[0] < 0, x[0] > 9)
        entities = jax.lax.select(
            time_to_move,
            entities.at[i].set(x * slot_filled * (1 - outside_of_frame)),
            old_entities,
        )

        # Update if entity moves into the player after its state is updated
        coords = jnp.logical_and(x[0] == state.player_x, x[1] == state.player_y)
        collision = jnp.logical_and(coords, slot_filled)
        # If collision with gold: empty gold and give positive reward
        collision_gold = jnp.logical_and(collision, x[3])
        reward += jax.lax.select(time_to_move, collision_gold, False) * 1
        entities = jax.lax.select(
            time_to_move,
            entities.at[i].set(entities[i] * (1 - collision_gold)),
            old_entities,
        )
        # If collision with enemy: terminate the episode
        collision_enemy = jnp.logical_and(collision, 1 - x[3])
        done += jax.lax.select(time_to_move, collision_enemy, False)
    return (
        state.replace(entities=entities, move_timer=move_timer),
        reward,
        bool(done > 0),
    )


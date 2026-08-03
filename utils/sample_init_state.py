from typing import Tuple

def sample_init_state(
    key: chex.PRNGKey, rows: int, columns: int
) -> Tuple[jnp.ndarray, jnp.ndarray, int, int]:
    """Sample a new initial state."""
    ball_x = jax.random.randint(key, shape=(), minval=0, maxval=columns)
    ball_y = 0
    paddle_x = columns // 2
    paddle_y = rows - 1
    return ball_x, jnp.array(ball_y), paddle_x, paddle_y


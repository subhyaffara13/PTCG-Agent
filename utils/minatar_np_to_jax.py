
def minatar_np_to_jax(env, env_name: str = "Asterix-MinAtar", get_jax: bool = False):
    """Collects env state of MinAtar into dict for JAX `step`."""
    state_gym_to_jax = None
    if env_name == "Asterix-MinAtar":
        entities_array = jnp.zeros((8, 5), dtype=jnp.int32)
        for i in range(8):
            if env.env.entities[i] is not None:
                entities_array = entities_array.at[i, 0:4].set(env.env.entities[i])
                entities_array = entities_array.at[i, 4].set(1)
        state_gym_to_jax = {
            "player_x": env.env.player_x,
            "player_y": env.env.player_y,
            "shot_timer": env.env.shot_timer,
            "spawn_speed": env.env.spawn_speed,
            "spawn_timer": env.env.spawn_timer,
            "move_speed": env.env.move_speed,
            "move_timer": env.env.move_timer,
            "ramp_timer": env.env.ramp_timer,
            "ramp_index": env.env.ramp_index,
            "entities": entities_array,
            "time": 0,
            "terminal": False,
        }
        if get_jax:

            return asterix.EnvState(**state_gym_to_jax)
    elif env_name == "Breakout-MinAtar":
        state_gym_to_jax = {
            "ball_y": jnp.array(env.env.ball_y),
            "ball_x": jnp.array(env.env.ball_x),
            "ball_dir": env.env.ball_dir,
            "pos": env.env.pos,
            "brick_map": jnp.array(env.env.brick_map),
            "strike": env.env.strike,
            "last_y": jnp.array(env.env.last_y),
            "last_x": jnp.array(env.env.last_x),
            "time": 0,
            "terminal": False,
        }
        if get_jax:

            return breakout.EnvState(**state_gym_to_jax)
    elif env_name == "Freeway-MinAtar":
        state_gym_to_jax = {
            "pos": env.env.pos,
            "cars": jnp.array(env.env.cars),
            "move_timer": env.env.move_timer,
            "time": 0,
            "terminal": False,
        }
        if get_jax:

            return freeway.EnvState(**state_gym_to_jax)
    # elif env_name == "Seaquest-MinAtar":
    #   f_bullets = np.zeros((100, 3))
    #   for i, f_b in enumerate(env.env.f_bullets):
    #     f_bullets[i] = f_b
    #   e_bullets = np.zeros((100, 3))
    #   for i, e_b in enumerate(env.env.e_bullets):
    #     e_bullets[i] = e_b
    #   e_fish = np.zeros((100, 5))
    #   for i, e_f in enumerate(env.env.e_fish):
    #     e_fish[i] = e_f + [10]
    #   e_subs = np.zeros((100, 5))
    #   for i, e_s in enumerate(env.env.e_subs):
    #     e_subs[i] = e_s
    #   divers = np.zeros((100, 4))
    #   for i, d in enumerate(env.env.divers):
    #     divers[i] = d

    #   state_gym_to_jax = {
    #       "oxygen": env.env.oxygen,
    #       "sub_x": env.env.sub_x,
    #       "sub_y": env.env.sub_y,
    #       "sub_or": env.env.sub_or,
    #       "f_bullet_count": len(env.env.f_bullets),
    #       "f_bullets": f_bullets,
    #       "e_bullet_count": len(env.env.e_bullets),
    #       "e_bullets": e_bullets,
    #       "e_fish_count": len(env.env.e_fish),
    #       "e_fish": e_fish,
    #       "e_subs_count": len(env.env.e_subs),
    #       "e_subs": e_subs,
    #       "diver_count": env.env.diver_count,
    #       "divers": divers,
    #       "e_spawn_speed": env.env.e_spawn_speed,
    #       "e_spawn_timer": env.env.e_spawn_timer,
    #       "d_spawn_timer": env.env.d_spawn_timer,
    #       "move_speed": env.env.move_speed,
    #       "ramp_index": env.env.ramp_index,
    #       "shot_timer": env.env.shot_timer,
    #       "surface": env.env.surface,
    #       "time": 0,
    #       "terminal": 0,
    #   }
    #   if get_jax:

    #     return seaquest.EnvState(**state_gym_to_jax)
    elif env_name == "SpaceInvaders-MinAtar":
        state_gym_to_jax = {
            "pos": env.env.pos,
            "f_bullet_map": jnp.array(env.env.f_bullet_map),
            "e_bullet_map": jnp.array(env.env.e_bullet_map),
            "alien_map": jnp.array(env.env.alien_map),
            "alien_dir": env.env.alien_dir,
            "enemy_move_interval": env.env.enemy_move_interval,
            "alien_move_timer": env.env.alien_move_timer,
            "alien_shot_timer": env.env.alien_shot_timer,
            "ramp_index": env.env.ramp_index,
            "shot_timer": env.env.shot_timer,
            "ramping": env.env.ramping,
            "time": 0,
            "terminal": False,
        }
        if get_jax:

            return space_invaders.EnvState(**state_gym_to_jax)
    return state_gym_to_jax



def _serialize_units(game):
    """Convert units to a list of dicts.

    The four ``*Cooldown`` fields are the per-unit "turns until I can
    reuse this ability" counters tracked on the engine but not visible
    in the duration counters (``paralyzedTurns`` etc.) above. Surfacing
    them lets agents avoid submitting ability actions that
    ``get_legal_actions`` would already mask out as illegal.
    """
    units = []
    for unit in game.units:
        units.append(
            {
                "type": unit.type,
                "owner": unit.player,
                "x": unit.x,
                "y": unit.y,
                "hp": unit.health,
                "maxHp": unit.max_health,
                "canMove": unit.can_move,
                "canAttack": unit.can_attack,
                "paralyzedTurns": unit.paralyzed_turns,
                "isHasted": unit.is_hasted,
                "distanceMoved": unit.distance_moved,
                "defenceBuffTurns": unit.defence_buff_turns,
                "attackBuffTurns": unit.attack_buff_turns,
                "paralyzeCooldown": unit.paralyze_cooldown,
                "hasteCooldown": unit.haste_cooldown,
                "defenceBuffCooldown": unit.defence_buff_cooldown,
                "attackBuffCooldown": unit.attack_buff_cooldown,
            }
        )
    return units


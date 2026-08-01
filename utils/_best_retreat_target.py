
def _best_retreat_target(retreat_actions, game_state, opponent_max_damage=0, opponent_type=""):
    """Pick the retreat target that balances attack capability, survivability, and type matchup."""
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    bench = list(getattr(game_state, 'my_bench', []))
    best_action = retreat_actions[0]
    best_score = -999

    # Check opponent's current energy for post-retreat evaluation
    opp_attached_energy = 0
    opp_active = getattr(game_state, 'opponent_active', None)
    if isinstance(opp_active, dict):
        opp_attached_energy = len(opp_active.get("attached", []) or opp_active.get("energies", []))

    for ra in retreat_actions:
        try:
            idx = int(ra.replace("retreat:", "").strip())
            if 0 <= idx < len(bench):
                bp = bench[idx]
                if isinstance(bp, dict):
                    ba = len(bp.get("attached", []) or bp.get("energies", []))
                    bid = bp.get("id")
                    if bid is not None:
                        tc = registry.get_full_skill(bid)
                        if tc:
                            ec = max(1, tc.energy_cost) if tc.energy_cost else 1
                            dmg = tc.damage_output or 0
                            hp = tc.hp or 100
                            score = dmg if ba >= ec else (-10 - idx)
                            # Survivability vs opponent max damage
                            if opponent_max_damage > 0:
                                if hp < opponent_max_damage:
                                    score -= 5.0  # Target dies immediately
                                elif hp <= opponent_max_damage * 1.5:
                                    score -= 1.0  # 2HKO range
                                if hp >= opponent_max_damage * 2:
                                    score += 1.5  # Safe tank
                            # Type resistance/weakness bonus
                            type_score = _get_poke_type_resistance(tc, opponent_type)
                            if type_score != 0.0:
                                score += type_score * 0.5  # +/-1.0 for type matchup
                            # Opponent energy check: can they KO the new active with existing energy?
                            if opp_attached_energy > 0:
                                opp_card = None
                                if isinstance(opp_active, dict):
                                    try:
                                        opp_card = registry.get_full_skill(opp_active.get("id"))
                                    except Exception:
                                        pass
                                if opp_card and opp_attached_energy >= max(1, opp_card.energy_cost):
                                    if opponent_max_damage >= hp:
                                        score -= 3.0  # Opponent already has energy to KO the swap-in
                            if score > best_score:
                                best_score = score
                                best_action = ra
        except Exception:
            pass
    return best_action


def _best_retreat_target(retreat_actions, game_state, opponent_max_damage=0, opponent_type=""):
    """Pick the retreat target that balances attack capability, survivability, and type matchup."""
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    bench = list(getattr(game_state, 'my_bench', []))
    best_action = retreat_actions[0]
    best_score = -999

    # Check opponent's current energy for post-retreat evaluation
    opp_attached_energy = 0
    opp_active = getattr(game_state, 'opponent_active', None)
    if isinstance(opp_active, dict):
        opp_attached_energy = len(opp_active.get("attached", []) or opp_active.get("energies", []))

    for ra in retreat_actions:
        try:
            idx = int(ra.replace("retreat:", "").strip())
            if 0 <= idx < len(bench):
                bp = bench[idx]
                if isinstance(bp, dict):
                    ba = len(bp.get("attached", []) or bp.get("energies", []))
                    bid = bp.get("id")
                    if bid is not None:
                        tc = registry.get_full_skill(bid)
                        if tc:
                            ec = max(1, tc.energy_cost) if tc.energy_cost else 1
                            dmg = tc.damage_output or 0
                            hp = tc.hp or 100
                            score = dmg if ba >= ec else (-10 - idx)
                            # Survivability vs opponent max damage
                            if opponent_max_damage > 0:
                                if hp < opponent_max_damage:
                                    score -= 5.0  # Target dies immediately
                                elif hp <= opponent_max_damage * 1.5:
                                    score -= 1.0  # 2HKO range
                                if hp >= opponent_max_damage * 2:
                                    score += 1.5  # Safe tank
                            # Type resistance/weakness bonus
                            type_score = _get_poke_type_resistance(tc, opponent_type)
                            if type_score != 0.0:
                                score += type_score * 0.5  # +/-1.0 for type matchup
                            # Opponent energy check: can they KO the new active with existing energy?
                            if opp_attached_energy > 0:
                                opp_card = None
                                if isinstance(opp_active, dict):
                                    try:
                                        opp_card = registry.get_full_skill(opp_active.get("id"))
                                    except Exception:
                                        pass
                                if opp_card and opp_attached_energy >= max(1, opp_card.energy_cost):
                                    if opponent_max_damage >= hp:
                                        score -= 3.0  # Opponent already has energy to KO the swap-in
                            if score > best_score:
                                best_score = score
                                best_action = ra
        except Exception:
            pass
    return best_action


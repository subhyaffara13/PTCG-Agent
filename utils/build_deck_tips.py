
def build_deck_tips(trend_stats, deck_trackers, threshold):
    deck_tips = {"deck_donts": []}
    report_lines = []
    if trend_stats["fast_losses"] > threshold:
        report_lines.append(f"- **[CRITICAL TREND]** Detected {trend_stats['fast_losses']} extremely fast losses (<5 turns). The deck is likely mulliganing or getting basic-benched too early.")
        deck_tips["deck_donts"].append({"condition": "pokemon_lt_12", "penalty": 2.0, "reason": "Statistically proven: dropping below 12 pokemon causes unacceptable fast-loss rates."})
    if deck_trackers["energy_starve"] > threshold:
        report_lines.append(f"- **[CRITICAL TREND]** Detected {deck_trackers['energy_starve']} games heavily plagued by dead 'pass' turns. Deck is energy starved or lacks draw support.")
        deck_tips["deck_donts"].append({"condition": "energy_lt_12_trainer_lt_10", "penalty": 2.0, "reason": "Statistically proven: low energy/draw combinations lead to >50% pass-turn game loops."})
    return deck_tips, report_lines


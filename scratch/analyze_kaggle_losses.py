import json
from pathlib import Path

from scratch.analyze_kaggle_losses_parts import get_deck_from_state


def main():
    loss_episodes = [81178524, 81178489, 81177772, 81174793, 81171012, 81170439, 81169868, 81168545]
    replays_dir = Path("logs/kaggle_replays")

    print("### KAGGLE LOSS MATCH DECK & STATE ANALYSIS\n")

    for ep_id in loss_episodes:
        replay_file = replays_dir / f"episode-{ep_id}-replay.json"
        if not replay_file.exists():
            continue

        data = json.loads(replay_file.read_text(encoding="utf-8"))
        steps = data.get("steps", [])
        info = data.get("info", {})
        team_names = info.get("TeamNames", ["Unknown", "Unknown"])
        agents = info.get("Agents", [])

        my_idx = -1
        opp_name = "Unknown"
        for idx, agent in enumerate(agents):
            name = agent.get("Name", "")
            if "Subhy" in name or "subhy" in name:
                my_idx = idx
            else:
                opp_name = name

        if my_idx == -1:
            for idx, name in enumerate(team_names):
                if "Subhy" in name or "subhy" in name:
                    my_idx = idx
                else:
                    opp_name = name

        last_step = steps[-1]
        my_final = last_step[my_idx] if my_idx < len(last_step) else {}
        opp_final = last_step[1 - my_idx] if (1 - my_idx) < len(last_step) else {}

        my_status = my_final.get("status")
        opp_status = opp_final.get("status")

        my_obs = my_final.get("observation", {}) or {}
        my_curr = my_obs.get("current", {}) or {}

        print(f"**Episode {ep_id} vs {opp_name} ({len(steps)} steps)**")
        print(f"- My Status: {my_status}, Opponent Status: {opp_status}")
        print(f"- Final Turn: {my_curr.get('turn')}, Action Count: {my_curr.get('turnActionCount')}")

        logs = my_obs.get("logs", [])
        if logs:
            print("- Final logs:")
            for log in logs[-5:]:
                print(f"  * {log}")

        players = my_curr.get("players", [])
        if len(players) > 1:
            my_p_state = players[my_idx] if my_idx < len(players) else {}
            opp_p_state = players[1 - my_idx] if (1 - my_idx) < len(players) else {}

            def list_len(val):
                return len(val) if val is not None else "Hidden"

            print(f"- My Prizes: {my_p_state.get('prizes')}, Deck: {list_len(my_p_state.get('deck'))}, Hand: {list_len(my_p_state.get('hand'))}, Bench: {list_len(my_p_state.get('bench'))}")
            print(f"- Opponent Prizes: {opp_p_state.get('prizes')}, Deck: {list_len(opp_p_state.get('deck'))}, Hand: {list_len(opp_p_state.get('hand'))}, Bench: {list_len(opp_p_state.get('bench'))}")
            print(f"  * My state keys: {list(my_p_state.keys())}")
            print(f"  * Opponent state keys: {list(opp_p_state.keys())}")

            my_active = my_p_state.get("active") or {}
            opp_active = opp_p_state.get("active") or {}
            my_active_id = my_active.get('card_id') if isinstance(my_active, dict) else my_active
            opp_active_id = opp_active.get('card_id') if isinstance(opp_active, dict) else opp_active
            print(f"- My Active: {my_active_id}")
            print(f"- Opponent Active: {opp_active_id}")
        print()


if __name__ == "__main__":
    main()

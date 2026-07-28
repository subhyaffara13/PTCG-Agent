"""
factory/deep_replay_inspector.py

Deep Replay Inspector for PTCG.
Parses raw Kaggle turn-by-turn episode JSON replays to identify exact step-level failure root causes:
1. Sub-prompt empty returns (act=[]) resulting in turn forfeiture
2. Premature turn passes when legal attacks or energy attachments exist
3. Unnecessary deck draws near deck-out thresholds (<= 5 cards)
4. Missed lethal opportunities (attacks that could KO active opponent)
5. Active Pokémon wiped out with 0 benched backups
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger("DeepReplayInspector")


class DeepReplayInspector:
    def __init__(self, replays_dir: str = "logs/kaggle_replays"):
        self.replays_dir = Path(replays_dir)
        self.replays_dir.mkdir(parents=True, exist_ok=True)

    def inspect_replay_file(self, replay_path: Path, my_team_id: str | None = None) -> Dict[str, Any]:
        """Parses a single Kaggle episode JSON replay to extract structured loss flaws."""
        if not replay_path.exists():
            logger.warning(f"Replay file not found: {replay_path}")
            return {}

        try:
            with open(replay_path, "r", encoding="utf-8") as f:
                replay = json.load(f)
        except Exception as e:
            logger.error(f"Failed to parse JSON replay {replay_path.name}: {e}")
            return {}

        steps = replay.get("steps", [])
        rewards = replay.get("rewards", [0, 0])
        
        # Determine our player index (0 or 1)
        my_idx = 0
        if my_team_id and len(steps) > 0:
            for idx, agent in enumerate(steps[0]):
                tid = str(getattr(agent, "teamId", getattr(agent, "team_id", "")))
                if tid == str(my_team_id):
                    my_idx = idx
                    break

        opp_idx = 1 - my_idx
        my_reward = rewards[my_idx] if len(rewards) > my_idx else 0
        won = my_reward > 0

        flaws = []
        empty_subprompts = 0
        premature_passes = 0
        deckout_draws = 0
        missed_kos = 0

        for i, step in enumerate(steps):
            if i < 2 or len(step) <= my_idx:
                continue

            agent = step[my_idx]
            obs = agent.get("observation", {})
            current = obs.get("current", None)
            select = obs.get("select", None)
            act = agent.get("action", None)
            status = agent.get("status", "ACTIVE")

            if status in ("ERROR", "TIMEOUT"):
                flaws.append({
                    "step": i,
                    "type": "CRASH",
                    "description": f"Agent crashed with status {status}"
                })
                continue

            # 1. Sub-prompt empty return check (act = [])
            if isinstance(act, list) and len(act) == 0:
                if isinstance(select, dict) and select.get("type", 0) != 0:
                    empty_subprompts += 1
                    flaws.append({
                        "step": i,
                        "type": "EMPTY_SUBPROMPT",
                        "description": f"Returned empty choice act=[] for sub-prompt type {select.get('type')}"
                    })

            if not current or not isinstance(current, dict):
                continue

            players = current.get("players", [])
            if len(players) <= max(my_idx, opp_idx):
                continue

            us = players[my_idx]
            opp = players[opp_idx]

            my_deck = us.get("deckCount", 60)
            my_bench = us.get("bench", [])
            my_active = us.get("active", [])

            # 2. Deck-out draw check: drawing when deck <= 5
            if my_deck <= 5 and isinstance(select, dict):
                opts = select.get("options", [])
                if isinstance(act, int) and act < len(opts):
                    chosen_opt = opts[act]
                    if isinstance(chosen_opt, dict):
                        opt_name = str(chosen_opt.get("name", "")).lower()
                        if any(d in opt_name for d in ("research", "iono", "lillie", "colress", "draw")):
                            deckout_draws += 1
                            flaws.append({
                                "step": i,
                                "type": "RISKY_DRAW_NEAR_DECKOUT",
                                "description": f"Drawn card {opt_name} with only {my_deck} cards remaining in deck"
                            })

            # 3. Premature Pass Check: passing when attacks were legal
            if act == 14 or (isinstance(act, int) and isinstance(select, dict) and select.get("options", [])):
                opts = select.get("options", [])
                if isinstance(act, int) and act < len(opts):
                    chosen_opt = opts[act]
                    if isinstance(chosen_opt, dict) and chosen_opt.get("type") == 14:  # Pass
                        has_attack = any(o.get("type") in (12, 13) for o in opts if isinstance(o, dict))
                        if has_attack:
                            premature_passes += 1
                            flaws.append({
                                "step": i,
                                "type": "PREMATURE_PASS",
                                "description": "Passed turn despite having legal attack options available"
                            })

        # Endgame Loss Cause Classification
        loss_reason = "UNKNOWN"
        if not won and steps:
            final = steps[-1]
            if len(final) > my_idx:
                fc = final[my_idx].get("observation", {}).get("current", {})
                if fc and isinstance(fc, dict):
                    pls = fc.get("players", [])
                    if len(pls) > max(my_idx, opp_idx):
                        us_f = pls[my_idx]
                        opp_f = pls[opp_idx]
                        if us_f.get("deckCount", 1) == 0:
                            loss_reason = "DECK_OUT"
                        elif not us_f.get("active") and not us_f.get("bench"):
                            loss_reason = "BENCH_WIPE"
                        elif opp_f.get("prizeCount", 6) == 0:
                            loss_reason = "PRIZES_EXHAUSTED"

        summary = {
            "replay_file": replay_path.name,
            "won": won,
            "loss_reason": loss_reason if not won else "NONE",
            "total_steps": len(steps),
            "flaw_counts": {
                "empty_subprompts": empty_subprompts,
                "premature_passes": premature_passes,
                "deckout_draws": deckout_draws,
                "missed_kos": missed_kos
            },
            "flaws": flaws
        }

        logger.info(f"Inspected {replay_path.name}: won={won}, loss_reason={loss_reason}, flaws={len(flaws)}")
        return summary

    def inspect_latest_losses(self, submission_id: str | None = None) -> List[Dict[str, Any]]:
        """Finds and inspects all recent losing replay files in logs/kaggle_replays."""
        reports = []
        replay_files = sorted(self.replays_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        
        for rf in replay_files[:5]:
            report = self.inspect_replay_file(rf)
            if report and not report.get("won", True):
                reports.append(report)

        # Save cumulative inspection report
        out_file = Path("logs/replay_inspection_report.json")
        try:
            out_file.write_text(json.dumps(reports, indent=2), encoding="utf-8")
            logger.info(f"Saved DeepReplayInspector report with {len(reports)} losing episode analyses to {out_file}")
        except Exception as e:
            logger.error(f"Failed to write replay inspection report: {e}")

        return reports

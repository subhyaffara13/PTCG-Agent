from typing import Any
import json
import logging
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
from factory.kaggle_scraper import KaggleScraper
from factory.do_pattern_extractor import DoPatternExtractor
from factory.anti_pattern_extractor import AntiPatternExtractor

from factory.teams.leaderboard_helper import (
    load_processed_players,
    save_processed_players,
    log_to_decisions,
    process_team_episodes,
    process_our_own_submissions,
)

logger = logging.getLogger("LeaderboardTeam")


class LeaderboardTeam:
    """Manages downloading, extracting rules, and processing top players' replays."""

    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", decisions_file: str = "decisions.md"):
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.decisions_file = Path(decisions_file)

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)

        self.processed_file = self.log_dir / "processed_leaderboard_players.json"
        self.processed_players = load_processed_players(self.processed_file)

        self.scraper = KaggleScraper(output_dir=str(self.log_dir / "kaggle_replays"))
        self.do_extractor = DoPatternExtractor(skills_dir=str(self.skills_dir))
        self.anti_extractor = AntiPatternExtractor(logs_dir=str(self.log_dir), skills_dir=str(self.skills_dir))

    def run_leaderboard_feedback_loop(self, competition_id: str = "pokemon-tcg-ai-battle") -> dict:
        logger.info("Leaderboard Team starting feedback loop...")
        results: dict[str, Any] = {"new_players_found": [], "downloaded_wins": 0, "downloaded_losses": 0}

        try:
            api = KaggleApi()
            api.authenticate()
            leaderboard = api.competition_leaderboard_view(competition_id)
            if not leaderboard:
                logger.warning("No leaderboard data found.")
                return results
            top_10 = leaderboard[:50]
        except Exception as e:
            logger.error(f"Kaggle API or Authentication failed: {e}")
            return results

        new_entries = []
        for entry in top_10:
            team_id = str(getattr(entry, 'team_id', getattr(entry, 'teamId', "")))
            team_name = getattr(entry, 'team_name', getattr(entry, 'teamName', ""))
            if team_id and team_id not in self.processed_players:
                logger.info(f"New top player identified: {team_name} (ID: {team_id})")
                new_entries.append((team_id, team_name))

        if new_entries:
            for team_id, team_name in new_entries:
                try:
                    logger.info(f"Processing matches for {team_name} (ID: {team_id})...")
                    wins, losses, sub_id = process_team_episodes(
                        api, team_id, team_name, self.scraper, self.do_extractor, self.anti_extractor
                    )
                    if sub_id is None:
                        continue

                    results["downloaded_wins"] += wins
                    results["downloaded_losses"] += losses
                    results["new_players_found"].append(team_name)

                    self.processed_players[team_id] = {
                        "team_name": team_name,
                        "submission_id": sub_id,
                        "wins_analyzed": wins,
                        "losses_analyzed": losses,
                    }
                    save_processed_players(self.processed_file, self.processed_players)
                    log_to_decisions(self.decisions_file, team_name, team_id, wins, losses)
                except Exception as e:
                    logger.error(f"Error processing team {team_name} (ID: {team_id}): {e}")
        else:
            logger.info("No new players emerged in the top 50.")

        # Metagame Distribution Analysis & Dynamic Counter-Deck Selection
        try:
            logger.info("Leaderboard Team analyzing metagame archetype distribution...")
            meta_counts = {}
            for entry in top_10[:20]:
                t_name = getattr(entry, 'team_name', getattr(entry, 'teamName', '')).lower()
                if "lightning" in t_name or "miraidon" in t_name: meta_counts["Lightning"] = meta_counts.get("Lightning", 0) + 1
                elif "water" in t_name or "bax" in t_name: meta_counts["Water"] = meta_counts.get("Water", 0) + 1
                elif "fire" in t_name or "zard" in t_name: meta_counts["Fire"] = meta_counts.get("Fire", 0) + 1
                else: meta_counts["Control"] = meta_counts.get("Control", 0) + 1
            
            dominant_meta = max(meta_counts, key=lambda k: meta_counts[k]) if meta_counts else "Lightning"
            logger.info(f"Metagame Analysis Complete. Dominant Meta: {dominant_meta} ({meta_counts.get(dominant_meta, 0)}/20 top decks)")
            results["dominant_metagame"] = dominant_meta
            
            # Save metagame distribution report for DeckArchitect
            meta_file = self.log_dir / "metagame_distribution.json"
            meta_file.write_text(json.dumps({"dominant_meta": dominant_meta, "distribution": meta_counts}, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Metagame distribution analysis failed: {e}")

        return results

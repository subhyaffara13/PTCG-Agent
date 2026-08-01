
def save_csv_report(results: List[Dict], csv_file: str):
    """Saves a CSV report with rubric scores, MVP, and key metrics."""
    if not results:
        print("No results to save to CSV.")
        return

    fieldnames = [
        "File", "Title", "Score", "Winner", "Outcome", "Turns",
        "Strategic Depth", "Unpredictability", "Narrative Quality", 
        "Humor", "Player Competence", "Pacing", "Subjective Impression", "Synergy",
        "MVP", "MVP Role", "MVP Reasoning"
    ]

    try:
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for res in results:
                metrics = res.get('entertainment_metrics', {})
                rubric = metrics.get('rubric', {})
                
                # Find MVP Role
                mvp_name = res.get('mvp_player', 'N/A')
                mvp_role = "Unknown"
                if mvp_name != 'N/A':
                    for p in res.get('player_stats', []):
                        if p.get('display_name') == mvp_name:
                            mvp_role = p.get('role', 'Unknown')
                            break

                row = {
                    "File": res.get("_filename", "Unknown"),
                    "Title": res.get("title", ""),
                    "Score": metrics.get("excitement_score", 0),
                    "Winner": res.get("winner_team", "Unknown"),
                    "Outcome": metrics.get("outcome_type", ""),
                    "Turns": res.get("total_turns", 0),
                    "Strategic Depth": rubric.get("strategic_depth", 0),
                    "Unpredictability": rubric.get("unpredictability", 0),
                    "Narrative Quality": rubric.get("narrative_quality", 0),
                    "Humor": rubric.get("humor", 0),
                    "Player Competence": rubric.get("player_competence", 0),
                    "Pacing": rubric.get("pacing", 0),
                    "Subjective Impression": rubric.get("subjective_impression", 0),
                    "Synergy": rubric.get("synergy", 0),
                    "MVP": mvp_name,
                    "MVP Role": mvp_role,
                    "MVP Reasoning": res.get("mvp_reasoning", "")
                }
                writer.writerow(row)
        print(f"CSV report saved to: {csv_file}")
    except Exception as e:
        print(f"Error saving CSV report: {e}")


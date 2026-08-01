
def run_winning_analysis(replay_paths: List[Path], player_name_or_id: str, extractor) -> None:
    card_counter = Counter()
    setup_durs, bench_dens, p_counts, t_counts, e_counts = [], [], [], [], []
    total_wins = 0
    deck_dos = []

    for path in replay_paths:
        if not path.exists(): continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            steps = data.get("steps", [])
            player_idx = _get_player_idx(steps, data.get("info", {}), data.get("info", {}).get("TeamNames", ["", ""]), player_name_or_id)
            if player_idx == -1 or len(data.get("rewards", [])) <= player_idx or data.get("rewards", [])[player_idx] <= 0:
                continue
            total_wins += 1
            _process_replay_steps(steps, player_idx, card_counter, setup_durs, bench_dens, p_counts, t_counts, e_counts)
        except Exception as e:
            logger.error(f"Error parsing replay {path}: {e}")

    if total_wins == 0: return

    # 1. Gemini LLM Winning Card Synergy Extraction
    import os
    import requests
    from dotenv import load_dotenv
    from cb_agents.card_registry import CardRegistry
    
    load_dotenv()
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    openai_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1") + "/chat/completions"
    llm_success = False
    
    if (gemini_key or openai_key) and card_counter:
        reg = CardRegistry()
        frequent_card_names = []
        for cid, cnt in card_counter.most_common(15):
            c = reg.get(cid)
            if c:
                frequent_card_names.append(f"{c.card_name} (card_id: {cid}, count_in_wins: {cnt})")
                
        if frequent_card_names:
            prompt = f"""
            You are an expert Pokémon TCG Deck Architect.
            We have analyzed a batch of winning replays for a top leaderboard player (team name: {player_name_or_id}).
            
            The player's winning deck relies heavily on these cards:
            {chr(10).join(frequent_card_names)}
            
            Identify the key strategy, card combos, and package synergies.
            Output a JSON object containing a list of `deck_dos` recommendations. Each item must have:
            - 'card_id' (integer, matching one of the card_ids provided)
            - 'avg_count' (float, recommended copies in deck)
            - 'reason' (string, detailing the exact synergy, combo, or strategic use case of this card in the winning build).
            """
            
            # Try Gemini first if available
            if gemini_key:
                logger.info("DoPatternAnalysis: Querying Google Gemini for winning deck synergies...")
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "responseMimeType": "application/json",
                        "responseSchema": {
                            "type": "OBJECT",
                            "properties": {
                                "deck_dos": {
                                    "type": "ARRAY",
                                    "items": {
                                        "type": "OBJECT",
                                        "properties": {
                                            "card_id": {"type": "INTEGER", "description": "The exact integer card_id from the prompt list."},
                                            "avg_count": {"type": "NUMBER", "description": "Recommended average number of copies in the deck."},
                                            "reason": {"type": "STRING", "description": "Details of the synergy, combo, or strategy behind this card choice."}
                                        },
                                        "required": ["card_id", "avg_count", "reason"]
                                    }
                                }
                            },
                            "required": ["deck_dos"]
                        }
                    }
                }
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={gemini_key}"
                    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
                    if res.status_code == 200:
                        data = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                        parsed = json.loads(data)
                        new_dos = parsed.get("deck_dos", [])
                        deck_dos = new_dos
                        
                        for item in new_dos:
                            existing = next((x for x in extractor.learned_dos["deck_dos"] if int(x.get("card_id", 0)) == int(item["card_id"])), None)
                            if existing:
                                existing["avg_count"] = max(existing.get("avg_count", 0), item["avg_count"])
                                existing["reason"] = item["reason"]
                            else:
                                extractor.learned_dos["deck_dos"].append(item)
                        logger.info(f"Successfully merged {len(new_dos)} Gemini-derived card synergies into learned_dos.")
                        llm_success = True
                except Exception as e:
                    logger.warning(f"Gemini synergy extraction failed: {e}.")

            # Try OpenAI fallback if Gemini was not available or failed
            if not llm_success and openai_key:
                logger.info("DoPatternAnalysis: Querying OpenAI LLM for winning deck synergies...")
                openai_payload = {
                    "model": "gpt-4o-mini",
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system", "content": "You are a Pokemon TCG AI analyst. Return JSON with key 'deck_dos' containing an array of objects with 'card_id' (int), 'avg_count' (float), and 'reason' (str)."},
                        {"role": "user", "content": prompt}
                    ]
                }
                try:
                    headers = {"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"}
                    res = requests.post(openai_url, json=openai_payload, headers=headers, timeout=30)
                    if res.status_code == 200:
                        content_str = res.json()["choices"][0]["message"]["content"]
                        parsed = json.loads(content_str)
                        new_dos = parsed.get("deck_dos", [])
                        deck_dos = new_dos
                        for item in new_dos:
                            existing = next((x for x in extractor.learned_dos["deck_dos"] if int(x.get("card_id", 0)) == int(item["card_id"])), None)
                            if existing:
                                existing["avg_count"] = max(existing.get("avg_count", 0), item["avg_count"])
                                existing["reason"] = item["reason"]
                            else:
                                extractor.learned_dos["deck_dos"].append(item)
                        logger.info(f"Successfully merged {len(new_dos)} OpenAI-derived card synergies into learned_dos.")
                        llm_success = True
                except Exception as e:
                    logger.warning(f"OpenAI synergy extraction failed: {e}.")

            # Try OpenRouter Free Models fallback if previous attempts failed
            openrouter_key = os.environ.get("OPENROUTER_API_KEY")
            if not llm_success and openrouter_key:
                logger.info("DoPatternAnalysis: Querying OpenRouter Free Model endpoint for winning deck synergies...")
                or_payload = {
                    "model": "google/gemini-2.5-flash:free",
                    "messages": [
                        {"role": "system", "content": "You are a Pokemon TCG AI analyst. Return JSON object with key 'deck_dos' containing an array of objects with 'card_id' (int), 'avg_count' (float), and 'reason' (str)."},
                        {"role": "user", "content": prompt}
                    ]
                }
                try:
                    headers = {"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"}
                    res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=or_payload, headers=headers, timeout=30)
                    if res.status_code == 200:
                        content_str = res.json()["choices"][0]["message"]["content"]
                        # Extract JSON string if wrapped in markdown block
                        if "```json" in content_str:
                            content_str = content_str.split("```json")[1].split("```")[0].strip()
                        elif "```" in content_str:
                            content_str = content_str.split("```")[1].split("```")[0].strip()
                        parsed = json.loads(content_str)
                        new_dos = parsed.get("deck_dos", [])
                        deck_dos = new_dos
                        for item in new_dos:
                            existing = next((x for x in extractor.learned_dos["deck_dos"] if int(x.get("card_id", 0)) == int(item["card_id"])), None)
                            if existing:
                                existing["avg_count"] = max(existing.get("avg_count", 0), item["avg_count"])
                                existing["reason"] = item["reason"]
                            else:
                                extractor.learned_dos["deck_dos"].append(item)
                        logger.info(f"Successfully merged {len(new_dos)} OpenRouter-derived card synergies into learned_dos.")
                        llm_success = True
                except Exception as e:
                    logger.warning(f"OpenRouter synergy extraction failed: {e}.")

    # 2. Baseline Frequency Checker Fallback
    if not llm_success:
        deck_dos = [{"card_id": int(cid), "avg_count": round(cnt / total_wins, 2), "reason": f"High usage in winning matches."}
                    for cid, cnt in card_counter.items() if (cnt / total_wins) >= 1.5]
                    
        for new_do in deck_dos:
            existing = next((item for item in extractor.learned_dos["deck_dos"] if item["card_id"] == new_do["card_id"]), None)
            if existing: existing["avg_count"] = max(existing.get("avg_count", 0), new_do["avg_count"])
            else: extractor.learned_dos["deck_dos"].append(new_do)

    if setup_durs:
        behavior_do = {"player": player_name_or_id, "avg_setup_duration": round(sum(setup_durs)/len(setup_durs), 1),
                       "avg_bench_density": round(sum(bench_dens)/len(bench_dens) if bench_dens else 0.0, 1)}
        extractor.learned_dos["behavior_dos"] = [b for b in extractor.learned_dos.get("behavior_dos", []) if b.get("player") != player_name_or_id] + [behavior_do]
        extractor.learned_dos["setup_profiles"] = [b for b in extractor.learned_dos.get("setup_profiles", []) if b.get("player") != player_name_or_id] + [behavior_do]

    if p_counts:
        extractor.learned_dos["deck_stats"] = {"avg_pokemon_count": round(sum(p_counts)/len(p_counts), 1),
                                               "avg_trainer_count": round(sum(t_counts)/len(t_counts), 1),
                                               "avg_energy_count": round(sum(e_counts)/len(e_counts), 1)}
    extractor._save_dos()
    logger.info(f"Extracted {len(deck_dos)} deck recommendations from {total_wins} matches.")


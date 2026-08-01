
def _extract_csv_row(file_path):
    """Helper to extract a single row for the CSV from a game file.
    
    Returns:
        tuple: (data_dict, error_message)
            - data_dict: The extracted data or None on failure.
            - error_message: Error string or None on success.
    """
    try:
        with open(file_path, 'r') as f:
            try:
                game = json.load(f)
            except json.JSONDecodeError:
                return None, f"JSONDecodeError in {file_path}"

        # Basic validation of structure
        if 'configuration' not in game or 'agents' not in game['configuration']:
            return None, f"Missing configuration/agents in {file_path}"

        agents = game['configuration']['agents']
        game_end = game.get('info', {}).get('GAME_END')

        # If the game didn't end properly, we might not have winner_ids
        if not game_end:
            return None, f"Missing GAME_END in {file_path}"

        winner_ids = set(game_end.get('winner_ids', []))
        
        # Recreate players to handle ID shuffling (randomize_ids)
        # This ensures we map the correct Agent (from config index) to the correct Player ID
        config = game.get('configuration', {})
        agents_config = config.get('agents', [])
        
        try:
            players = create_players_from_agents_config(
                agents_config,
                randomize_roles=config.get('randomize_roles', False),
                randomize_ids=config.get('randomize_ids', False),
                seed=config.get('seed')
            )
        except Exception as e:
            # Fallback if creation fails (e.g. valid seed missing), though unlikely for valid replays
            return None, f"Error creating players: {e}"

        model_ids = [p.agent.display_name for p in players]
        roles = [p.role.name for p in players]
        scores = [1 if p.id in winner_ids else 0 for p in players]

        # Calculate costs/tokens
        # We need to map player IDs to their costs. 
        # The costs logic relies on finding costs in steps for a given player ID.
        player_costs = defaultdict(float)
        player_prompt = defaultdict(int)
        player_completion = defaultdict(int)

        # Iterate steps (similar to _compute_costs)
        steps = game.get('steps', [])
        
        # We need a mapping from index in step to player ID.
        # But wait, step is list of agent-wise observations?
        # In Kaggle Werewolf, step is list of dicts. step[i] corresponds to... Player ID? Or Agent Index?
        # In raw obs, step[i] is for agent i (Kaggle Agent Index).
        # But the cost is inside 'action' which is inside 'step[i]'.
        # Is step[i] always for the SAME agent index i? Yes.
        # But does Agent Index i correspond to the same Player ID?
        # players[i] corresponds to Agent Index i.
        # So players[i].id is the ID for the agent at index i.
        
        for step in steps:
            for i, agent_idx in enumerate(step):
                if i >= len(players): continue # Should not happen
                p_id = players[i].id
                
                action = agent_idx.get('action', {})
                kwargs = action.get('kwargs', {})
                
                cost = kwargs.get('cost')
                prompt_t = kwargs.get('prompt_tokens')
                completion_t = kwargs.get('completion_tokens')
                
                if cost: player_costs[p_id] += float(cost)
                if prompt_t: player_prompt[p_id] += int(prompt_t)
                if completion_t: player_completion[p_id] += int(completion_t)
                
        # Create lists aligned with players (who are aligned with Agents)
        costs = [player_costs[p.id] for p in players]
        prompt_tokens = [player_prompt[p.id] for p in players]
        completion_tokens = [player_completion[p.id] for p in players]

        return {
            'models': model_ids,
            'scores': scores,
            'roles': roles,
            'costs': costs,
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens
        }, None
    except Exception as e:
        return None, f"Error processing {file_path}: {str(e)}"


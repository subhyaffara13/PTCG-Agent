import json
import os
from typing import Tuple

def extract_game_transcript(json_path: str) -> Tuple[str, int]:
    if not os.path.exists(json_path):
        return f"Error: File {json_path} not found.", 0

    with open(json_path, "r") as f:
        try:
            game_data = json.load(f)
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}", 0

    name_manager = NameManager(game_data)

    steps = game_data.get("steps", [])
    info = game_data.get("info", {})
    game_end = info.get("GAME_END", {})
    config_agents = game_data.get("configuration", {}).get("agents", [])
    
    # Extract Team/Role info for all players to help context
    player_roles = {}
    source_agents = game_end.get("all_players", []) if (game_end and "all_players" in game_end) else []
    if not source_agents and config_agents:
        source_agents = [{"agent": a, "id": a.get("id")} for a in config_agents]
        
    for p in source_agents:
        agent_data = p.get("agent", {}) if "agent" in p else p
        pid = agent_data.get("id", p.get("id", "Unknown"))
        role = agent_data.get("role", "Unknown")
        team = agent_data.get("team", "Unknown")
        player_roles[pid] = {"role": role, "team": team}

    transcript = []
    transcript.append(f"GAME RECORD: {os.path.basename(json_path)}")
    transcript.append("=" * 50)
    
    # 1. Roster
    transcript.append("ROSTER:")
    for pid, info in player_roles.items():
        display_name = name_manager.get_name(pid)
        line = f"- {display_name}"
        if display_name != pid:
            line += f" (ID: {pid})"
        line += f" -> Role: {info['role']} ({info['team']})"
        transcript.append(line)
    transcript.append("=" * 50)

    # State tracking
    current_phase = "GAME START"
    seen_event_signatures = set()

    seen_event_signatures = set()

    for step_idx, step in enumerate(steps):
        # Gather events for this step
        step_events = []
        
        # Check specific events to detect phase changes or major game events
        for agent_state in step:
            obs = agent_state.get("observation", {})
            raw_obs = obs.get("raw_observation", {})
            event_views = raw_obs.get("new_player_event_views", [])
            for event in event_views:
                # Use Global Deduplication for Moderator events based on created_at + description
                # This handles cases where the same event is re-sent in subsequent steps
                if event.get("source") == "MODERATOR":
                    sig = f"{event.get('created_at')}_{event.get('description')}"
                else:
                    # For player actions, we might need step context, but usually created_at is strictly unique
                    sig = f"{event.get('created_at')}_{event.get('description')}"

                if sig in seen_event_signatures:
                    continue
                seen_event_signatures.add(sig)
                
                step_events.append(event)
        
        # Sort events by time
        step_events.sort(key=lambda x: x.get("created_at", ""))
        
        # Process Events (Global / Moderator)
        for event in step_events:
            event_name = event.get("event_name")
            data = event.get("data") or {}
            desc = event.get("description", "").strip()
            
            # Detect Phase Changes
            # Try to get day from data first, then top-level event
            day_count = data.get("day_count")
            if day_count is None:
                day_count = event.get("day")
                
            if event_name == "day_start":
                current_phase = f"DAY {day_count}"
                transcript.append(f"\n=== {current_phase} ===\n")
            elif event_name == "night_start":
                current_phase = f"NIGHT {day_count}"
                transcript.append(f"\n=== {current_phase} ===\n")
            
            # Skip noise
            if event_name in ["vote_request", "chat_request", "phase_change", "phase_divider"]:
                continue
                
            # Skip "Your player id is..." boilerplates
            if "Your player id is" in desc:
                continue

            # Format specific events
            if event_name == "elimination":
                pid = data.get("eliminated_player_id")
                role = data.get("eliminated_player_role_name")
                if pid:
                    d_pid = name_manager.get_name(pid)
                    transcript.append(f"[ELIMINATION] {d_pid} ({role}) was eliminated.")
                continue
            
            if event_name == "role_reveal":
                continue
            
            if desc:
                # General moderator messages
                clean_desc = name_manager.replace_names(desc)
                # Filter out raw list dumps in Day Start
                if "Alive Players:" in clean_desc: continue 
                if "Role Counts:" in clean_desc: continue
                # Filter out voting start messages that are redundant
                if "Voting starts from player" in clean_desc: continue
                # Filter out "Wake up X" messages if they don't add value (optional, but requested to clean up)
                
                transcript.append(f"[Global] {clean_desc}")

        # Process Actions (Speech, Votes, Abilities)
        for agent_idx, agent_state in enumerate(step):
            action = agent_state.get("action")
            if not action:
                continue
            
            obs = agent_state.get("observation", {})
            raw_obs = obs.get("raw_observation", {})
            player_id = raw_obs.get("player_id", obs.get("player_id", f"Agent_{agent_idx}"))
            display_player = name_manager.get_name(player_id)
            player_role = player_roles.get(player_id, {}).get("role", "?")
            
            kwargs = action.get("kwargs", {}) if isinstance(action, dict) else {}
            raw_completion = kwargs.get("raw_completion")
            
            if raw_completion:
                try:
                    parsed = json.loads(format_json_string(raw_completion))
                    message = parsed.get("message")
                    reasoning = parsed.get("reasoning")
                    target = parsed.get("target_id")
                    
                    # Add context about the action type if available
                    # We can infer type from the phase or data
                    
                    if message:
                        msg_display = name_manager.replace_names(message)
                        transcript.append(f"{display_player}: \"{msg_display}\"")
                        if reasoning:
                            res_display = name_manager.replace_names(reasoning)
                            transcript.append(f"  > Thought: {res_display}")
                    elif target:
                         target_display = name_manager.get_name(target)
                         action_type = "Acted on"
                         if "Vote" in current_phase or "Voting" in current_phase:
                             action_type = "Voted for"
                         elif player_role == "Doctor":
                             action_type = "Protected"
                         elif player_role == "Seer":
                             action_type = "Inspected"
                         elif player_role == "Werewolf":
                             action_type = "Targeted"
                         
                         transcript.append(f"{display_player} [{action_type}] {target_display}")
                         if reasoning:
                             res_display = name_manager.replace_names(reasoning)
                             transcript.append(f"  > Thought: {res_display}")

                except:
                    pass

    return "\n".join(transcript), len(steps)


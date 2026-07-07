class OrchestratorBeliefMixin:
    def sync_belief_tracker(self, game_state: dict):
        """Synchronizes the belief tracker state with the current public game state.
        Calls update_on_* methods for detected opponent actions to keep known_in_hand accurate.
        """
        def get_id(obj):
            if obj is None:
                return None
            if isinstance(obj, (int, str)):
                try:
                    return int(obj)
                except (ValueError, TypeError):
                    return None
            # Try dict key
            if isinstance(obj, dict):
                val = obj.get("id")
                if val is not None:
                    try:
                        return int(val)
                    except (ValueError, TypeError):
                        pass
            # Try attribute
            for attr in ("id", "card_id"):
                if hasattr(obj, attr):
                    val = getattr(obj, attr)
                    if val is not None:
                        try:
                            return int(val)
                        except (ValueError, TypeError):
                            pass
            return None

        prev_hand_size = self.belief_tracker.state.hand_size
        prev_discard_len = len(self.belief_tracker.state.known_in_discard)

        self.belief_tracker.state.hand_size = game_state.get("opponent_hand_count", 5)
        self.belief_tracker.state.prize_size = game_state.get("opponent_prizes", 6)

        # Detect draw: hand grew
        hand_diff = self.belief_tracker.state.hand_size - prev_hand_size
        if hand_diff > 0:
            self.belief_tracker.update_on_draw(hand_diff)

        known_in_play = {}
        active = game_state.get("opponent_active")
        if active:
            active_id = get_id(active)
            if active_id is not None:
                known_in_play[active_id] = 1
                # Detect play: active changed from previous sync
                prev_play = self.belief_tracker.state.known_in_play
                if active_id not in prev_play:
                    self.belief_tracker.update_on_play(active_id)

        for bench_item in game_state.get("opponent_bench", []):
            bench_id = get_id(bench_item)
            if bench_id is not None:
                known_in_play[bench_id] = known_in_play.get(bench_id, 0) + 1

        self.belief_tracker.state.known_in_play = known_in_play

        known_in_discard = {}
        for card_id in game_state.get("opponent_discard", []):
            card_id_int = get_id(card_id)
            if card_id_int is not None:
                known_in_discard[card_id_int] = known_in_discard.get(card_id_int, 0) + 1

        # Detect discard: new cards in discard
        for cid, cnt in known_in_discard.items():
            prev_cnt = self.belief_tracker.state.known_in_discard.get(cid, 0)
            if cnt > prev_cnt:
                self.belief_tracker.update_on_discard(cid)

        self.belief_tracker.state.known_in_discard = known_in_discard

        total_cards = sum(self.belief_tracker.assumed_deck.values()) if self.belief_tracker.assumed_deck else 60
        known_non_deck = (self.belief_tracker.state.hand_size + 
                          self.belief_tracker.state.prize_size + 
                          sum(known_in_play.values()) + 
                          sum(known_in_discard.values()))
        self.belief_tracker.state.deck_size = max(0, total_cards - known_non_deck)
        self.belief_tracker._recalculate_probabilities()

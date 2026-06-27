# Task Completion

1. Created `factory/game_validator.py` with `validate_mcts_step` checking:
   - empty `my_hand`
   - `ATTACK_KO` with 0 damage
   - `select_prize` defaulting to pass
2. Updated `factory/game_adapter.py`:
   - Supported `cardId` and `name` in `_get_id`
   - Parsed `legal_retreats`, `legal_evolutions`, and `select_prize`

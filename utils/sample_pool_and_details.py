
def sample_pool_and_details():
    card_pool = [
        {"card_id": "1", "card_name": "Charmander", "card_type": "Pokemon", "archetype": "aggro"},
        {"card_id": "2", "card_name": "Charmeleon", "card_type": "Pokemon", "archetype": "aggro"},
        {"card_id": "3", "card_name": "Charizard", "card_type": "Pokemon", "archetype": "aggro"},
        {"card_id": "4", "card_name": "Basic {R} Energy", "card_type": "Energy", "archetype": "utility"},
        {"card_id": "5", "card_name": "Basic {W} Energy", "card_type": "Energy", "archetype": "utility"},
        {"card_id": "6", "card_name": "Nest Ball", "card_type": "Trainer", "archetype": "utility"},
        {"card_id": "7", "card_name": "Squirtle", "card_type": "Pokemon", "archetype": "aggro"},
        {"card_id": "8", "card_name": "Wartortle", "card_type": "Pokemon", "archetype": "aggro"},
    ]
    card_details = {
        "1": {"card_id": "1", "card_name": "Charmander", "card_type": "Pokemon", "stage": "Basic", "element_type": "{R}"},
        "2": {"card_id": "2", "card_name": "Charmeleon", "card_type": "Pokemon", "stage": "Stage 1", "previous_stage": "Charmander", "element_type": "{R}"},
        "3": {"card_id": "3", "card_name": "Charizard", "card_type": "Pokemon", "stage": "Stage 2", "previous_stage": "Charmeleon", "element_type": "{R}"},
        "4": {"card_id": "4", "card_name": "Basic {R} Energy", "card_type": "Energy", "stage": "Basic", "element_type": "{R}"},
        "5": {"card_id": "5", "card_name": "Basic {W} Energy", "card_type": "Energy", "stage": "Basic", "element_type": "{W}"},
        "6": {"card_id": "6", "card_name": "Nest Ball", "card_type": "Trainer", "stage": "Basic", "element_type": ""},
        "7": {"card_id": "7", "card_name": "Squirtle", "card_type": "Pokemon", "stage": "Basic", "element_type": "{W}"},
        "8": {"card_id": "8", "card_name": "Wartortle", "card_type": "Pokemon", "stage": "Stage 1", "previous_stage": "Squirtle", "element_type": "{W}"},
    }
    return card_pool, card_details


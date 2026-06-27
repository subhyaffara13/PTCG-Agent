import json

CARD_POOL_BASIC = {
    "cards": [
        {"card_id": "SV-1", "card_name": "Pikachu", "card_type": "Pokemon", "archetype": "aggro", "combo_tags": ["Basic"]},
        {"card_id": "SV-2", "card_name": "Lightning Energy", "card_type": "Energy", "archetype": "utility", "combo_tags": []},
        {"card_id": "SV-3", "card_name": "Raichu", "card_type": "Pokemon", "archetype": "aggro", "combo_tags": ["Stage 1"]}
    ]
}

CARD_POOL_REALISTIC = {
    "cards": [
        {"card_id": "frigibax-par-057", "card_name": "Frigibax", "card_type": "Pokemon", "archetype": "aggro", "combo_tags": ["Basic"]},
        {"card_id": "baxcalibur-par-060", "card_name": "Baxcalibur", "card_type": "Pokemon", "archetype": "aggro", "combo_tags": ["Stage 2"]},
        {"card_id": "charmander-obs-023", "card_name": "Charmander", "card_type": "Pokemon", "archetype": "combo", "combo_tags": ["Basic"]},
        {"card_id": "basic-water-energy", "card_name": "Basic {W} Energy", "card_type": "Energy", "archetype": "utility", "combo_tags": []},
        {"card_id": "basic-fire-energy", "card_name": "Basic {R} Energy", "card_type": "Energy", "archetype": "utility", "combo_tags": []},
        {"card_id": "nest-ball-sv1-255", "card_name": "Nest Ball", "card_type": "Trainer", "archetype": "utility", "combo_tags": ["search"]},
        {"card_id": "ultra-ball-sv1-196", "card_name": "Ultra Ball", "card_type": "Trainer", "archetype": "utility", "combo_tags": ["search"]},
        {"card_id": "professor-s-research-sv1-190", "card_name": "Professor's Research", "card_type": "Trainer", "archetype": "utility", "combo_tags": ["Supporter", "draw"]}
    ]
}

CSV_DATA = (
    "Card ID,Card Name,Stage (Pok\u00e9mon)/Type (Energy and Trainer),Previous stage,Type\n"
    "frigibax-par-057,Frigibax,Basic Pok\u00e9mon,n/a,{W}\n"
    "baxcalibur-par-060,Baxcalibur,Stage 2 Pok\u00e9mon,Arctibax,{W}\n"
    "charmander-obs-023,Charmander,Basic Pok\u00e9mon,n/a,{R}\n"
    "basic-water-energy,Basic {W} Energy,Basic Energy,n/a,{W}\n"
    "basic-fire-energy,Basic {R} Energy,Basic Energy,n/a,{R}\n"
)

ARCHETYPES_DATA = {
    "archetypes": {
        "aggro": {"signature_cards": ["baxcalibur-par-060"], "card_pool": ["frigibax-par-057"]}
    }
}

def make_skills_dir(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    return skills_dir

def make_decisions_file(tmp_path):
    decisions_file = tmp_path / "decisions.md"
    decisions_file.write_text("# Decisions\n", encoding="utf-8")
    return decisions_file

def make_staging_dir(tmp_path):
    staging_dir = tmp_path / "staging"
    staging_dir.mkdir()
    return staging_dir

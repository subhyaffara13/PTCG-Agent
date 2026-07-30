from cb_agents.card_types import CardType, CardStage, TrainerSubtype, ComboTag

CARD_TYPE_MAP = {
    'pokemon': CardType.POKEMON,
    'trainer': CardType.TRAINER,
    'energy': CardType.ENERGY
}

STAGE_MAP = {
    'basic': CardStage.BASIC,
    'stage 1': CardStage.STAGE1,
    'stage 2': CardStage.STAGE2
}

TRAINER_MAP = {
    'item': TrainerSubtype.ITEM,
    'supporter': TrainerSubtype.SUPPORTER,
    'tool': TrainerSubtype.TOOL,
    'stadium': TrainerSubtype.STADIUM,
    'pokémon tool': TrainerSubtype.TOOL
}

COMBO_TAG_MAP = {
    'search': ComboTag.SEARCH,
    'bench': ComboTag.BENCH,
    'damage': ComboTag.DAMAGE,
    'draw': ComboTag.DRAW,
    'attach': ComboTag.ATTACH,
    'energy': ComboTag.ENERGY,
    'switch': ComboTag.SWITCH,
    'discard': ComboTag.DISCARD,
    'shuffle': ComboTag.SHUFFLE,
    'evolve': ComboTag.EVOLVE,
    'heal': ComboTag.HEAL,
    'ko': ComboTag.KO,
    'Basic': ComboTag.BASIC,
    'Supporter': ComboTag.SUPPORTER,
    'Stage 1': ComboTag.STAGE1,
    'Stage 2': ComboTag.STAGE2
}

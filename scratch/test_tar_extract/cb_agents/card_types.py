from enum import IntEnum, IntFlag

class CardType(IntEnum):
    UNKNOWN = 0
    POKEMON = 1
    TRAINER = 2
    ENERGY = 3

class CardStage(IntEnum):
    NONE = 0
    BASIC = 1
    STAGE1 = 2
    STAGE2 = 3

class TrainerSubtype(IntEnum):
    NONE = 0
    ITEM = 1
    SUPPORTER = 2
    TOOL = 3
    STADIUM = 4

class ComboTag(IntFlag):
    NONE = 0
    SEARCH = 1
    BENCH = 2
    DAMAGE = 4
    DRAW = 8
    ATTACH = 16
    ENERGY = 32
    SWITCH = 64
    DISCARD = 128
    SHUFFLE = 256
    EVOLVE = 512
    HEAL = 1024
    KO = 2048
    BASIC = 4096
    SUPPORTER = 8192
    STAGE1 = 16384
    STAGE2 = 32768

# String-to-enum mapping helpers
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

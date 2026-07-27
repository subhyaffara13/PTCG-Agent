#ifndef PTCG_TYPES_H
#define PTCG_TYPES_H

#include <string>
#include <vector>
#include <unordered_map>

enum class CardType {
    UNKNOWN = 0,
    POKEMON = 1,
    TRAINER = 2,
    ENERGY = 3
};

enum class CardStage {
    NONE = 0,
    BASIC = 1,
    STAGE1 = 2,
    STAGE2 = 3
};

enum class TrainerSubtype {
    NONE = 0,
    ITEM = 1,
    SUPPORTER = 2,
    TOOL = 3,
    STADIUM = 4
};

struct Card {
    std::string card_id;
    std::string card_name;
    CardType card_type = CardType::UNKNOWN;
    CardStage stage = CardStage::NONE;
    TrainerSubtype trainer_subtype = TrainerSubtype::NONE;
    int combo_tags = 0;
    float ev_score = 0.0f;
    int damage_output = 0;
    int energy_cost = 0;
    float utility_score = 0.0f;
    std::string archetype;
    std::string element_type;
    std::string previous_stage;
    bool is_full = false;
};

struct PokemonInstance {
    std::string id;
    int hp = 100;
    std::vector<std::string> attached;
};

struct PlayerState {
    std::vector<std::string> hand;
    PokemonInstance active;
    bool has_active = false;
    std::vector<PokemonInstance> bench;
    std::vector<std::string> discard;
    std::vector<std::string> deck;
    int deck_count = 60;
    int prizes = 6;
    bool deck_out_loss = false;
    bool supporter_played_this_turn = false;
};

struct BoardState {
    PlayerState me;
    PlayerState opponent;
    bool turn_ended = false;
    bool game_over = false;
    std::string winner = "";
    int turn_number = 1;
    std::vector<std::string> legal_actions;
};

#endif // PTCG_TYPES_H

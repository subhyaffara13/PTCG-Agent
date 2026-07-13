#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "ptcg_types.h"
#include "ptcg_simulator.h"
#include "cpp_mcts.h"
#include <iostream>

namespace py = pybind11;

PokemonInstance dict_to_pokemon(const py::dict& d) {
    PokemonInstance p;
    if (d.contains("id") && !d["id"].is_none()) {
        p.id = py::str(d["id"]);
    }
    if (d.contains("hp") && !d["hp"].is_none()) {
        p.hp = d["hp"].cast<int>();
    }
    if (d.contains("attached") && !d["attached"].is_none()) {
        p.attached = d["attached"].cast<std::vector<std::string>>();
    }
    return p;
}

py::dict pokemon_to_dict(const PokemonInstance& p) {
    py::dict d;
    d["id"] = p.id;
    d["hp"] = p.hp;
    d["attached"] = p.attached;
    return d;
}

PlayerState dict_to_player(const py::dict& d, const std::string& prefix) {
    PlayerState p;
    std::string hand_key = prefix + "_hand";
    std::string active_key = prefix + "_active_pokemon";
    std::string active_hp_key = prefix + "_active_hp";
    std::string active_id_key = prefix + "_active_id";
    std::string active_dict_key = prefix + "_active";
    std::string bench_key = prefix + "_bench";
    std::string discard_key = prefix + "_discard";
    std::string deck_key = prefix + "_deck";
    std::string deck_count_key = prefix + "_deck_count";
    std::string prizes_key = prefix + "_prizes";
    std::string prizes_key_fallback = prefix + "_prizes_remaining";

    if (d.contains(hand_key) && !d[hand_key.c_str()].is_none()) {
        p.hand = d[hand_key.c_str()].cast<std::vector<std::string>>();
    }
    
    if (d.contains(active_key) && !d[active_key.c_str()].is_none()) {
        try {
            p.active = dict_to_pokemon(d[active_key.c_str()].cast<py::dict>());
            p.has_active = true;
        } catch (...) {}
    } else if (d.contains(active_dict_key) && !d[active_dict_key.c_str()].is_none()) {
        try {
            p.active = dict_to_pokemon(d[active_dict_key.c_str()].cast<py::dict>());
            p.has_active = true;
        } catch (...) {}
    }
    
    if (d.contains(active_hp_key) && !d[active_hp_key.c_str()].is_none()) {
        p.active.hp = d[active_hp_key.c_str()].cast<int>();
    }
    if (d.contains(active_id_key) && !d[active_id_key.c_str()].is_none()) {
        p.active.id = py::str(d[active_id_key.c_str()]);
        p.has_active = true;
    }
    
    if (d.contains(bench_key) && !d[bench_key.c_str()].is_none()) {
        auto bench_list = d[bench_key.c_str()].cast<py::list>();
        for (auto item : bench_list) {
            if (!item.is_none()) {
                p.bench.push_back(dict_to_pokemon(item.cast<py::dict>()));
            }
        }
    }
    
    if (d.contains(discard_key) && !d[discard_key.c_str()].is_none()) {
        p.discard = d[discard_key.c_str()].cast<std::vector<std::string>>();
    }
    if (d.contains(deck_key) && !d[deck_key.c_str()].is_none()) {
        p.deck = d[deck_key.c_str()].cast<std::vector<std::string>>();
    }
    if (d.contains(deck_count_key) && !d[deck_count_key.c_str()].is_none()) {
        p.deck_count = d[deck_count_key.c_str()].cast<int>();
    }
    if (d.contains(prizes_key) && !d[prizes_key.c_str()].is_none()) {
        p.prizes = d[prizes_key.c_str()].cast<int>();
    } else if (d.contains(prizes_key_fallback) && !d[prizes_key_fallback.c_str()].is_none()) {
        p.prizes = d[prizes_key_fallback.c_str()].cast<int>();
    }
    
    std::string deck_out_key = prefix + "_deck_out_loss";
    if (d.contains(deck_out_key) && !d[deck_out_key.c_str()].is_none()) {
        p.deck_out_loss = d[deck_out_key.c_str()].cast<bool>();
    }
    
    return p;
}

BoardState dict_to_boardstate(const py::dict& d) {
    BoardState s;
    s.me = dict_to_player(d, "my");
    s.opponent = dict_to_player(d, "opponent");
    
    if (d.contains("turn_ended") && !d["turn_ended"].is_none()) {
        s.turn_ended = d["turn_ended"].cast<bool>();
    }
    if (d.contains("game_over") && !d["game_over"].is_none()) {
        s.game_over = d["game_over"].cast<bool>();
    }
    if (d.contains("winner") && !d["winner"].is_none()) {
        s.winner = py::str(d["winner"]);
    }
    if (d.contains("turn_number") && !d["turn_number"].is_none()) {
        s.turn_number = d["turn_number"].cast<int>();
    }
    if (d.contains("legal_actions") && !d["legal_actions"].is_none()) {
        s.legal_actions = d["legal_actions"].cast<std::vector<std::string>>();
    }
    return s;
}

py::dict boardstate_to_dict(const BoardState& s) {
    py::dict d;
    d["turn_ended"] = s.turn_ended;
    d["game_over"] = s.game_over;
    d["winner"] = s.winner.empty() ? py::none() : py::cast(s.winner);
    d["turn_number"] = s.turn_number;
    d["legal_actions"] = s.legal_actions;
    
    d["my_hand"] = s.me.hand;
    if (s.me.has_active) {
        d["my_active_pokemon"] = pokemon_to_dict(s.me.active);
        d["my_active_hp"] = s.me.active.hp;
        d["my_active_id"] = s.me.active.id;
    } else {
        d["my_active_pokemon"] = py::none();
        d["my_active_hp"] = 0;
        d["my_active_id"] = py::none();
    }
    
    py::list my_bench_list;
    for (const auto& p : s.me.bench) {
        my_bench_list.append(pokemon_to_dict(p));
    }
    d["my_bench"] = my_bench_list;
    d["my_discard"] = s.me.discard;
    d["my_discard_pile"] = s.me.discard;
    d["my_deck"] = s.me.deck;
    d["my_deck_count"] = s.me.deck_count;
    d["my_prizes"] = s.me.prizes;
    d["my_prizes_remaining"] = s.me.prizes;
    d["my_deck_out_loss"] = s.me.deck_out_loss;
    
    if (s.opponent.has_active) {
        d["opponent_active"] = pokemon_to_dict(s.opponent.active);
        d["opponent_active_pokemon"] = pokemon_to_dict(s.opponent.active);
        d["opponent_active_hp"] = s.opponent.active.hp;
        d["opponent_active_id"] = s.opponent.active.id;
    } else {
        d["opponent_active"] = py::none();
        d["opponent_active_pokemon"] = py::none();
        d["opponent_active_hp"] = 0;
        d["opponent_active_id"] = py::none();
    }
    
    py::list opp_bench_list;
    for (const auto& p : s.opponent.bench) {
        opp_bench_list.append(pokemon_to_dict(p));
    }
    d["opponent_bench"] = opp_bench_list;
    d["opponent_hand"] = s.opponent.hand;
    d["opponent_discard"] = s.opponent.discard;
    d["opponent_discard_pile"] = s.opponent.discard;
    d["opponent_deck"] = s.opponent.deck;
    d["opponent_deck_count"] = s.opponent.deck_count;
    d["opponent_prizes"] = s.opponent.prizes;
    d["opponent_prizes_remaining"] = s.opponent.prizes;
    d["opponent_deck_out_loss"] = s.opponent.deck_out_loss;
    
    return d;
}

py::dict apply_action_py(py::dict game_state, const std::string& action) {
    BoardState state = dict_to_boardstate(game_state);
    apply_action(state, action);
    regenerate_legal_actions(state);
    return boardstate_to_dict(state);
}

py::list get_legal_actions_py(py::dict game_state) {
    BoardState state = dict_to_boardstate(game_state);
    regenerate_legal_actions(state);
    std::vector<std::string> canonical = mask_illegal(state.legal_actions, state);
    py::list res;
    for (const auto& a : canonical) {
        res.append(a);
    }
    return res;
}

std::string mcts_search_py(py::dict game_state, double time_limit_sec, int num_simulations, double c_puct) {
    BoardState state = dict_to_boardstate(game_state);
    if (state.legal_actions.empty()) {
        regenerate_legal_actions(state);
    }
    cpp_MCTSEngine engine(c_puct, num_simulations);
    return engine.search(state, time_limit_sec);
}

void initialize_registry_py(const std::string& skills_dir) {
    CardRegistry::getInstance().loadFromFiles(skills_dir);
}

void add_card_py(py::dict c) {
    Card card;
    card.card_id = py::str(c["card_id"]);
    card.card_name = py::str(c["card_name"]);
    
    std::string type_str = py::str(c["card_type"]);
    if (type_str == "Pokemon" || type_str == "pokemon") card.card_type = CardType::POKEMON;
    else if (type_str == "Trainer" || type_str == "trainer") card.card_type = CardType::TRAINER;
    else if (type_str == "Energy" || type_str == "energy") card.card_type = CardType::ENERGY;
    
    std::string stage_str = c.contains("stage_type") ? py::str(c["stage_type"]) : "";
    std::transform(stage_str.begin(), stage_str.end(), stage_str.begin(), ::tolower);
    if (stage_str.find("supporter") != std::string::npos) card.trainer_subtype = TrainerSubtype::SUPPORTER;
    else if (stage_str.find("item") != std::string::npos) card.trainer_subtype = TrainerSubtype::ITEM;
    else if (stage_str.find("tool") != std::string::npos) card.trainer_subtype = TrainerSubtype::TOOL;
    else if (stage_str.find("stadium") != std::string::npos) card.trainer_subtype = TrainerSubtype::STADIUM;
    if (stage_str.find("basic") != std::string::npos) card.stage = CardStage::BASIC;
    else if (stage_str.find("stage 1") != std::string::npos) card.stage = CardStage::STAGE1;
    else if (stage_str.find("stage 2") != std::string::npos) card.stage = CardStage::STAGE2;
    
    if (c.contains("previous_stage")) {
        card.previous_stage = py::str(c["previous_stage"]);
    }
    if (c.contains("energy_cost")) {
        card.energy_cost = c["energy_cost"].cast<int>();
    }
    if (c.contains("damage_output")) {
        card.damage_output = c["damage_output"].cast<int>();
    }
    CardRegistry::getInstance().addCard(card);
}

// -----------------------------------------------------------------------
// score_action / score_state wrappers for Python delegation
// -----------------------------------------------------------------------
py::object score_action_py(const py::dict& game_state, const std::string& action) {
    BoardState state;
    state.me = dict_to_player(game_state, "my");
    state.opponent = dict_to_player(game_state, "opponent");
    state.turn_number = game_state.contains("turn_number") ? game_state["turn_number"].cast<int>() : 1;
    double score = score_action(action, state, 0.0);
    return py::cast(score);
}

py::object score_state_py(const py::dict& game_state) {
    BoardState state;
    state.me = dict_to_player(game_state, "my");
    state.opponent = dict_to_player(game_state, "opponent");
    state.turn_number = game_state.contains("turn_number") ? game_state["turn_number"].cast<int>() : 1;
    double score = score_state(state);
    return py::cast(score);
}

PYBIND11_MODULE(ptcg_core, m) {
    m.doc() = "High-performance Pokemon TCG MCTS simulator engine";

    m.def("apply_action", &apply_action_py, "Apply an action to the game state dictionary",
          py::arg("game_state"), py::arg("action"));

    m.def("get_legal_actions", &get_legal_actions_py, "Get list of legal actions for the game state dictionary",
          py::arg("game_state"));

    m.def("mcts_search", &mcts_search_py, "Run MCTS UCT search on game state dictionary",
          py::arg("game_state"), py::arg("time_limit_sec") = 1.0, py::arg("num_simulations") = 50, py::arg("c_puct") = 1.25);

    m.def("initialize_registry", &initialize_registry_py, "Initialize card registry from skills directory",
          py::arg("skills_dir"));

    m.def("add_card", &add_card_py, "Manually add/override card in registry",
          py::arg("card_dict"));

    m.def("score_action", &score_action_py,
          "Score an action string given game state — C++ port of heuristic_pipeline_eval.score_action()",
          py::arg("game_state"), py::arg("action"));

    m.def("score_state", &score_state_py,
          "Score a board state — C++ port of heuristic_pipeline_eval.score_state()",
          py::arg("game_state"));
}


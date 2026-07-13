#include "ptcg_simulator.h"
#include <unordered_set>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cctype>

void CardRegistry::loadFromFiles(const std::string& skillsDir) {
    clear();
    loadMetadata(skillsDir + "/card_metadata.json");
    loadScoring(skillsDir + "/card_scoring.json");
    
    std::ifstream csvFile(skillsDir + "/card_pool_raw.csv");
    if (csvFile.is_open()) {
        std::string csvLine;
        std::getline(csvFile, csvLine); // Skip header
        while (std::getline(csvFile, csvLine)) {
            std::vector<std::string> fields;
            std::string currentField = "";
            bool inQuotes = false;
            for (size_t i = 0; i < csvLine.size(); ++i) {
                char c = csvLine[i];
                if (c == '"') {
                    inQuotes = !inQuotes;
                } else if (c == ',' && !inQuotes) {
                    fields.push_back(currentField);
                    currentField = "";
                } else {
                    currentField += c;
                }
            }
            fields.push_back(currentField);
            
            if (fields.size() > 15) {
                std::string moveName = lowercase(fields[13]);
                std::string damageStr = fields[15];
                if (!moveName.empty() && moveName != "n/a") {
                    moveDamage[moveName] = damageStr;
                }
            }
        }
    }
}

void CardRegistry::addCard(const Card& card) {
    cards[card.card_id] = card;
    std::string lowerName = lowercase(card.card_name);
    nameToId[lowerName] = card.card_id;
}

const Card* CardRegistry::getCard(const std::string& id) const {
    auto it = cards.find(id);
    if (it != cards.end()) {
        return &it->second;
    }
    return nullptr;
}

std::string CardRegistry::getIdByName(const std::string& name) const {
    auto it = nameToId.find(lowercase(name));
    if (it != nameToId.end()) {
        return it->second;
    }
    return "";
}

void CardRegistry::loadMetadata(const std::string& path) {
    std::ifstream file(path);
    if (!file.is_open()) {
        std::cerr << "[CardRegistry] Warning: Could not open metadata file: " << path << std::endl;
        return;
    }
    std::string line;
    Card currentCard;
    bool inCard = false;
    while (std::getline(file, line)) {
        if (line.find('{') != std::string::npos && line.find(':') != std::string::npos && line.find("cards") == std::string::npos) {
            currentCard = Card();
            inCard = true;
        } else if (inCard && line.find('}') != std::string::npos) {
            if (!currentCard.card_id.empty()) {
                addCard(currentCard);
            }
            inCard = false;
        } else if (inCard) {
            size_t colon = line.find(':');
            if (colon != std::string::npos) {
                std::string key = line.substr(0, colon);
                std::string val = line.substr(colon + 1);
                
                auto trim = [](std::string s) {
                    size_t start = s.find('"');
                    if (start == std::string::npos) return std::string("");
                    size_t end = s.find('"', start + 1);
                    if (end == std::string::npos) return std::string("");
                    return s.substr(start + 1, end - start - 1);
                };
                
                std::string keyStr = trim(key);
                std::string valStr = trim(val);
                
                if (keyStr == "card_id") {
                    currentCard.card_id = valStr;
                } else if (keyStr == "card_name") {
                    currentCard.card_name = valStr;
                } else if (keyStr == "card_type") {
                    if (valStr == "Pokemon" || valStr == "pokemon") currentCard.card_type = CardType::POKEMON;
                    else if (valStr == "Trainer" || valStr == "trainer") currentCard.card_type = CardType::TRAINER;
                    else if (valStr == "Energy" || valStr == "energy") currentCard.card_type = CardType::ENERGY;
                } else if (keyStr == "stage_type") {
                    std::string st = valStr;
                    std::transform(st.begin(), st.end(), st.begin(), ::tolower);
                    if (st.find("basic") != std::string::npos) currentCard.stage = CardStage::BASIC;
                    else if (st.find("stage 1") != std::string::npos) currentCard.stage = CardStage::STAGE1;
                    else if (st.find("stage 2") != std::string::npos) currentCard.stage = CardStage::STAGE2;
                } else if (keyStr == "previous_stage") {
                    currentCard.previous_stage = valStr;
                }
            }
        }
    }
}

void CardRegistry::loadScoring(const std::string& path) {
    std::ifstream file(path);
    if (!file.is_open()) {
        std::cerr << "[CardRegistry] Warning: Could not open scoring file: " << path << std::endl;
        return;
    }
    std::string line;
    std::string currentId;
    int energyCost = 0;
    int damageOutput = 0;
    bool inCard = false;
    while (std::getline(file, line)) {
        if (line.find('{') != std::string::npos) {
            currentId = "";
            energyCost = 0;
            damageOutput = 0;
            inCard = true;
        } else if (inCard && line.find('}') != std::string::npos) {
            if (!currentId.empty()) {
                auto it = cards.find(currentId);
                if (it != cards.end()) {
                    it->second.energy_cost = energyCost;
                    it->second.damage_output = damageOutput;
                }
            }
            inCard = false;
        } else if (inCard) {
            size_t colon = line.find(':');
            if (colon != std::string::npos) {
                std::string key = line.substr(0, colon);
                std::string val = line.substr(colon + 1);
                
                auto trim = [](std::string s) {
                    size_t start = s.find('"');
                    if (start == std::string::npos) return std::string("");
                    size_t end = s.find('"', start + 1);
                    if (end == std::string::npos) return std::string("");
                    return s.substr(start + 1, end - start - 1);
                };
                
                auto trimInt = [](std::string s) {
                    std::string res;
                    for (char c : s) {
                        if (std::isdigit(c)) res += c;
                    }
                    return res.empty() ? 0 : std::stoi(res);
                };
                
                std::string keyStr = trim(key);
                if (keyStr == "card_id") {
                    currentId = trim(val);
                } else if (keyStr == "energy_cost") {
                    energyCost = trimInt(val);
                } else if (keyStr == "damage_output") {
                    damageOutput = trimInt(val);
                }
            }
        }
    }
}

// Helpers
static void remove_from_hand(std::vector<std::string>& hand, const std::string& card_id) {
    auto it = std::find(hand.begin(), hand.end(), card_id);
    if (it != hand.end()) {
        hand.erase(it);
    } else {
        for (size_t i = 0; i < hand.size(); ++i) {
            if (hand.at(i) == card_id) {
                hand.erase(hand.begin() + i);
                break;
            }
        }
    }
}

static void draw_cards(BoardState& state, int n) {
    int dc = state.me.deck_count;
    int drawn = std::min(n, dc);
    state.me.deck_count = dc - drawn;
    if (n > dc) {
        state.me.deck_out_loss = true;
    }
    for (int i = 0; i < drawn; ++i) {
        if (!state.me.deck.empty()) {
            state.me.hand.push_back(state.me.deck.back());
            state.me.deck.pop_back();
        } else {
            state.me.hand.push_back("0");
        }
    }
}

static void apply_evolve(BoardState& state, const std::string& card_id) {
    remove_from_hand(state.me.hand, card_id);
    
    std::string search_id = card_id;
    auto reg_card = CardRegistry::getInstance().getCard(card_id);
    if (reg_card && !reg_card->previous_stage.empty()) {
        search_id = reg_card->previous_stage;
    }
    
    std::string search_lower = search_id;
    std::transform(search_lower.begin(), search_lower.end(), search_lower.begin(), ::tolower);
    
    bool evolved = false;
    for (size_t i = 0; i < state.me.bench.size(); ++i) {
        auto& poke = state.me.bench.at(i);
        std::string poke_id_lower = poke.id;
        std::transform(poke_id_lower.begin(), poke_id_lower.end(), poke_id_lower.begin(), ::tolower);
        
        bool match = (poke_id_lower == search_lower);
        if (!match) {
            auto poke_card = CardRegistry::getInstance().getCard(poke.id);
            if (poke_card) {
                std::string name_lower = poke_card->card_name;
                std::transform(name_lower.begin(), name_lower.end(), name_lower.begin(), ::tolower);
                if (name_lower == search_lower || poke_card->card_id == search_id) {
                    match = true;
                }
            }
        }
        if (match) {
            poke.id = "evolved_" + card_id;
            poke.hp = 150;
            evolved = true;
            break;
        }
    }
    
    if (!evolved && state.me.has_active) {
        std::string active_id_lower = state.me.active.id;
        std::transform(active_id_lower.begin(), active_id_lower.end(), active_id_lower.begin(), ::tolower);
        
        bool match = (active_id_lower == search_lower);
        if (!match) {
            auto active_card = CardRegistry::getInstance().getCard(state.me.active.id);
            if (active_card) {
                std::string name_lower = active_card->card_name;
                std::transform(name_lower.begin(), name_lower.end(), name_lower.begin(), ::tolower);
                if (name_lower == search_lower || active_card->card_id == search_id) {
                    match = true;
                }
            }
        }
        if (match) {
            state.me.active.id = "evolved_" + card_id;
            state.me.active.hp = 150;
        }
    }
}

void apply_action(BoardState& state, const std::string& action) {
    if (action.empty()) return;
    size_t first_colon = action.find(':');
    std::string act_type = (first_colon == std::string::npos) ? action : action.substr(0, first_colon);
    std::string target = (first_colon == std::string::npos) ? "" : action.substr(first_colon + 1);
    
    if (act_type == "pass") {
        state.turn_ended = true;
    }
    else if (act_type == "bench") {
        remove_from_hand(state.me.hand, target);
        PokemonInstance p;
        p.id = target;
        p.hp = 100;
        state.me.bench.push_back(p);
    }
    else if (act_type == "evolve") {
        apply_evolve(state, target);
    }
    else if (act_type == "attach_energy") {
        size_t second_colon = target.find(':');
        std::string card_id = (second_colon == std::string::npos) ? target : target.substr(0, second_colon);
        std::string poke_id = (second_colon == std::string::npos) ? "" : target.substr(second_colon + 1);
        
        std::vector<PokemonInstance*> valid_targets;
        if (state.me.has_active) {
            valid_targets.push_back(&state.me.active);
        }
        for (size_t i = 0; i < state.me.bench.size(); ++i) {
            valid_targets.push_back(&state.me.bench.at(i));
        }
        
        if (!valid_targets.empty()) {
            remove_from_hand(state.me.hand, card_id);
            PokemonInstance* chosen = nullptr;
            if (!poke_id.empty()) {
                for (auto* p : valid_targets) {
                    if (p->id == poke_id) {
                        chosen = p;
                        break;
                    }
                }
            }
            if (!chosen) {
                chosen = valid_targets.at(0);
            }
            chosen->attached.push_back(card_id);
        }
    }
    else if (act_type == "retreat") {
        if (!state.me.bench.empty()) {
            size_t target_idx = 0;
            if (!target.empty()) {
                try {
                    target_idx = std::stoul(target);
                } catch (...) {
                    for (size_t i = 0; i < state.me.bench.size(); ++i) {
                        if (state.me.bench.at(i).id == target) {
                            target_idx = i;
                            break;
                        }
                    }
                }
            }
            if (target_idx >= state.me.bench.size()) {
                target_idx = 0;
            }
            
            PokemonInstance old_active = state.me.active;
            PokemonInstance new_active = state.me.bench.at(target_idx);
            state.me.bench.erase(state.me.bench.begin() + target_idx);
            
            int retreat_cost = 1;
            int removed_count = std::min(retreat_cost, (int)old_active.attached.size());
            for (int r = 0; r < removed_count; ++r) {
                state.me.discard.push_back(old_active.attached.at(0));
                old_active.attached.erase(old_active.attached.begin());
            }
            
            state.me.bench.push_back(old_active);
            state.me.active = new_active;
            state.me.has_active = true;
        }
    }
    else if (act_type == "attack") {
        int actual_damage = 0;
        std::string move_name = target;
        std::string dmg_str = CardRegistry::getInstance().getMoveDamage(move_name);
        
        if (!dmg_str.empty()) {
            std::string lower_dmg = dmg_str;
            std::transform(lower_dmg.begin(), lower_dmg.end(), lower_dmg.begin(), ::tolower);
            if (lower_dmg.find('x') != std::string::npos || lower_dmg.find("×") != std::string::npos || lower_dmg.find('?') != std::string::npos) {
                actual_damage = 0;
            } else {
                if (!lower_dmg.empty() && lower_dmg.back() == '+') {
                    lower_dmg.pop_back();
                }
                std::string clean_dmg = "";
                for (char c : lower_dmg) {
                    if (std::isdigit(c)) clean_dmg += c;
                }
                actual_damage = clean_dmg.empty() ? 0 : std::stoi(clean_dmg);
            }
        } else {
            auto active_card = CardRegistry::getInstance().getCard(state.me.active.id);
            if (active_card) {
                actual_damage = active_card->damage_output;
            }
            if (actual_damage <= 0) {
                actual_damage = 100;
            }
        }
        
        state.opponent.active.hp = std::max(0, state.opponent.active.hp - actual_damage);
        if (state.opponent.active.hp <= 0) {
            int prize_yield = 1;
            auto opp_active_card = CardRegistry::getInstance().getCard(state.opponent.active.id);
            if (opp_active_card) {
                std::string n = opp_active_card->card_name;
                std::transform(n.begin(), n.end(), n.begin(), ::tolower);
                if (n.find("vmax") != std::string::npos) {
                    prize_yield = 3;
                } else if (n.find("vstar") != std::string::npos ||
                           n.rfind(" v") == n.size() - 2 ||
                           n.rfind(" ex") == n.size() - 3 ||
                           n.find(" ex ") != std::string::npos ||
                           n.find(" v ") != std::string::npos) {
                    prize_yield = 2;
                }
            }
            state.me.prizes = std::max(0, state.me.prizes - prize_yield);
            for (int py = 0; py < prize_yield; ++py) {
                state.me.hand.push_back("0");
            }
            
            if (!state.opponent.bench.empty()) {
                state.opponent.active = state.opponent.bench.at(0);
                state.opponent.bench.erase(state.opponent.bench.begin());
            } else {
                state.opponent.active.hp = 0;
                state.opponent.has_active = false;
            }
        }
        state.turn_ended = true;
    }
    else if (act_type == "play_trainer") {
        std::string trainer_name = target;
        std::string suffix = "";
        if (trainer_name.rfind("_heads") == trainer_name.size() - 6 && trainer_name.size() > 6) {
            suffix = "_heads";
            trainer_name = trainer_name.substr(0, trainer_name.size() - 6);
        } else if (trainer_name.rfind("_tails") == trainer_name.size() - 6 && trainer_name.size() > 6) {
            suffix = "_tails";
            trainer_name = trainer_name.substr(0, trainer_name.size() - 6);
        }
        
        std::string found_card_id = "";
        for (size_t i = 0; i < state.me.hand.size(); ++i) {
            const auto& cid = state.me.hand.at(i);
            auto c = CardRegistry::getInstance().getCard(cid);
            std::string hand_card_name = c ? c->card_name : "";
            std::transform(hand_card_name.begin(), hand_card_name.end(), hand_card_name.begin(), ::tolower);
            std::string target_lower = trainer_name;
            std::transform(target_lower.begin(), target_lower.end(), target_lower.begin(), ::tolower);
            if (hand_card_name == target_lower || cid == trainer_name) {
                found_card_id = cid;
                state.me.hand.erase(state.me.hand.begin() + i);
                break;
            }
        }
        if (found_card_id.empty()) {
            if (suffix.empty()) {
                remove_from_hand(state.me.hand, target);
            }
        }
        
        if (!found_card_id.empty()) {
            state.me.discard.push_back(found_card_id);
        } else {
            if (suffix.empty()) {
                state.me.discard.push_back(target);
            }
        }
        
        if (suffix != "_tails") {
            std::string base_name = trainer_name;
            std::transform(base_name.begin(), base_name.end(), base_name.begin(), ::tolower);
            if (base_name.find("research") != std::string::npos || base_name.find("professor") != std::string::npos) {
                state.me.discard.insert(state.me.discard.end(), state.me.hand.begin(), state.me.hand.end());
                state.me.hand.clear();
                draw_cards(state, 7);
            } else if (base_name.find("iono") != std::string::npos || base_name.find("judge") != std::string::npos) {
                state.me.deck.insert(state.me.deck.end(), state.me.hand.begin(), state.me.hand.end());
                state.me.deck_count += state.me.hand.size();
                state.me.hand.clear();
                draw_cards(state, 4);
            } else if (base_name.find("ball") != std::string::npos || base_name.find("ultra") != std::string::npos) {
                std::string added = "1";
                if (!state.me.deck.empty()) {
                    added = state.me.deck.back();
                    state.me.deck.pop_back();
                }
                state.me.hand.push_back(added);
                state.me.deck_count = std::max(0, state.me.deck_count - 1);
            } else if (base_name.find("secret box") != std::string::npos || base_name.find("petrel") != std::string::npos) {
                std::string added1 = "1";
                std::string added2 = "2";
                if (state.me.deck.size() >= 2) {
                    added1 = state.me.deck.back();
                    state.me.deck.pop_back();
                    added2 = state.me.deck.back();
                    state.me.deck.pop_back();
                }
                state.me.hand.push_back(added1);
                state.me.hand.push_back(added2);
                state.me.deck_count = std::max(0, state.me.deck_count - 2);
            }
        }
    }
    else if (act_type == "ability") {
        std::string name = target;
        std::transform(name.begin(), name.end(), name.begin(), ::tolower);
        if (name.find("colress") != std::string::npos ||
            name.find("concealed") != std::string::npos ||
            name.find("flower selecting") != std::string::npos ||
            name.find("shining arcana") != std::string::npos) {
            draw_cards(state, 3);
        }
    }
    
    check_win_conditions(state);
}

void regenerate_legal_actions(BoardState& state) {
    if (state.turn_ended) {
        state.legal_actions.clear();
        return;
    }
    std::vector<std::string> actions;
    actions.push_back("pass");
    
    std::vector<std::string> valid_targets;
    if (state.me.has_active) {
        valid_targets.push_back(state.me.active.id);
    }
    for (const auto& p : state.me.bench) {
        valid_targets.push_back(p.id);
    }
    
    for (const auto& card : state.me.hand) {
        auto c = CardRegistry::getInstance().getCard(card);
        if (c) {
            if (c->card_type == CardType::ENERGY) {
                if (!valid_targets.empty()) {
                    for (const auto& tgt : valid_targets) {
                        actions.push_back("attach_energy:" + card + ":" + tgt);
                    }
                } else {
                    actions.push_back("attach_energy:" + card);
                }
                continue;
            } else if (c->card_type == CardType::TRAINER) {
                actions.push_back("play_trainer:" + c->card_name);
                continue;
            }
        }
        actions.push_back("attach_energy:" + card);
        if (state.me.bench.size() < 5) {
            actions.push_back("bench:" + card);
        }
    }
    
    for (size_t i = 0; i < state.me.bench.size(); ++i) {
        actions.push_back("retreat:" + std::to_string(i));
    }
    
    if (state.opponent.active.hp > 0 && state.me.has_active) {
        int attached_count = (int)state.me.active.attached.size();
        auto card = CardRegistry::getInstance().getCard(state.me.active.id);
        int min_cost = (card && card->energy_cost > 0) ? card->energy_cost : 1;
        bool can_attack = attached_count >= min_cost;
        if (can_attack) {
            actions.push_back("attack:strike");
        }
    }
    
    std::vector<std::string> unique_actions;
    std::unordered_set<std::string> seen;
    for (const auto& act : actions) {
        if (seen.find(act) == seen.end()) {
            seen.insert(act);
            unique_actions.push_back(act);
        }
    }
    state.legal_actions = unique_actions;
}

void check_win_conditions(BoardState& state) {
    if (state.me.prizes <= 0) {
        state.game_over = true;
        state.winner = "me";
        return;
    }
    if (state.opponent.prizes <= 0) {
        state.game_over = true;
        state.winner = "opponent";
        return;
    }
    if (state.me.deck_out_loss || state.me.deck_count < 0) {
        state.game_over = true;
        state.winner = "opponent";
        return;
    }
    if (state.opponent.deck_out_loss || state.opponent.deck_count < 0) {
        state.game_over = true;
        state.winner = "me";
        return;
    }
    bool me_alive = !state.me.has_active || state.me.active.hp > 0;
    bool me_has_bench = !state.me.bench.empty();
    if (!me_alive && !me_has_bench) {
        state.game_over = true;
        state.winner = "opponent";
        return;
    }
    int opp_hp = state.opponent.has_active ? state.opponent.active.hp : 0;
    bool opp_has_bench = !state.opponent.bench.empty();
    if (opp_hp <= 0 && !opp_has_bench) {
        state.game_over = true;
        state.winner = "me";
        return;
    }
}

double score_state(const BoardState& state) {
    double v = 0.0;
    // Prize delta — key indicator of who is winning
    v += 0.15 * (state.opponent.prizes - state.me.prizes);
    // HP delta — secondary indicator
    if (state.me.has_active && state.opponent.has_active) {
        v += 0.001 * (state.me.active.hp - state.opponent.active.hp);
    }
    // Evolution stage bonus — evolved board = better setup
    std::vector<const PokemonInstance*> all_p;
    if (state.me.has_active) all_p.push_back(&state.me.active);
    for (const auto& p : state.me.bench) all_p.push_back(&p);
    int ec = 0;
    for (auto* p : all_p) {
        auto ce = CardRegistry::getInstance().getCard(p->id);
        if (ce && (ce->stage == CardStage::STAGE1 || ce->stage == CardStage::STAGE2)) ec++;
    }
    v += 0.05 * ec;
    return v;
}

double score_action(const std::string& action, const BoardState& state, double threat_penalty) {
    double v = 0.0;
    int dc  = state.me.deck_count;
    int mp  = state.me.prizes;
    int ahp = state.me.has_active ? state.me.active.hp : 100;
    int bn_size = (int)state.me.bench.size();
    int opp_hp  = state.opponent.has_active ? state.opponent.active.hp : 100;

    if (action.rfind("attack:", 0) == 0) {
        // Check if attack is actually feasible
        bool can_attack = false;
        if (state.me.has_active) {
            int attached_count = (int)state.me.active.attached.size();
            auto card = CardRegistry::getInstance().getCard(state.me.active.id);
            int min_cost = (card && card->energy_cost > 0) ? card->energy_cost : 1;
            can_attack = attached_count >= min_cost;
        }
        if (!can_attack) {
            v -= 0.5;  // Penalize attacks that can't be executed
        } else {
            v += 0.65;
        }
        if (mp <= 1) v += 1.0;  // game-winning attack
        if (mp <= 2) v += 0.3;  // close to winning
        // Type advantage
        if (state.me.has_active && state.opponent.has_active) {
            auto my_card = CardRegistry::getInstance().getCard(state.me.active.id);
            auto opp_card = CardRegistry::getInstance().getCard(state.opponent.active.id);
            // Simple proxy: check if we have type advantage via ev_score differential
            if (my_card && opp_card && my_card->ev_score > opp_card->ev_score) {
                v += 0.2;  // matchup advantage
            }
        }
        // KO potential
        if (state.me.has_active) {
            auto my_card = CardRegistry::getInstance().getCard(state.me.active.id);
            if (my_card && my_card->damage_output > 0 && my_card->damage_output >= opp_hp) {
                v += 1.5;  // KO bonus — very likely the winning move
            }
        }
    }
    else if (action.rfind("evolve:", 0) == 0) {
        v += 0.6;
    }
    else if (action.rfind("attach_energy:", 0) == 0) {
        v += 0.45;  // energy is critical for enabling attacks
        if (state.me.has_active) {
            int need = 2;
            auto e = CardRegistry::getInstance().getCard(state.me.active.id);
            if (e && e->energy_cost > 0) need = e->energy_cost;
            int att = (int)state.me.active.attached.size();
            if (att < need) {
                v += 0.35;  // charging up underfunded active
            } else {
                // Check if it's a special card that can use extra energy
                std::string an = e ? e->card_name : "";
                std::transform(an.begin(), an.end(), an.begin(), ::tolower);
                bool sc = (an.find("raging bolt") != std::string::npos
                        || an.find("iron hands") != std::string::npos
                        || an.find("chien pao") != std::string::npos
                        || an.find("ceruledge") != std::string::npos
                        || an.find("roaring moon") != std::string::npos);
                bool nr = (ahp <= 50);
                if (!sc && !nr) v -= 0.25;  // over-charging active
            }
        }
    }
    else if (action.rfind("bench:", 0) == 0) {
        if (bn_size == 0)      v += 0.8;
        else if (bn_size < 2)  v += 0.4;
        else if (bn_size < 3)  v += 0.25;
        else if (bn_size < 4)  v += 0.15;
        else if (bn_size < 5)  v += 0.05;
        else                   v -= 0.1;
    }
    else if (action.rfind("play_trainer:", 0) == 0) {
        v += 0.4;
        std::string tn = action.substr(13);
        std::transform(tn.begin(), tn.end(), tn.begin(), ::tolower);
        if (dc <= 5) {
            if (tn.find("iono") != std::string::npos || tn.find("judge") != std::string::npos)
                v += 0.8;
            else if (tn.find("research") != std::string::npos || tn.find("professor") != std::string::npos)
                v -= 1.3;
        }
        if (dc > 30) {
            const std::vector<std::string> search_keys = {
                "nest ball", "ultra ball", "quick ball", "level ball",
                "secret box", "mega signal", "team rocket's petrel"
            };
            for (const auto& k : search_keys) {
                if (tn.find(k) != std::string::npos) {
                    v += std::min(0.25, dc * 0.005);
                    break;
                }
            }
        }
    }
    else if (action.rfind("ability:", 0) == 0) {
        std::string tn = action.substr(8);
        std::transform(tn.begin(), tn.end(), tn.begin(), ::tolower);
        v += 0.35;
        if (dc <= 5 && (tn.find("colress") != std::string::npos || tn.find("concealed") != std::string::npos))
            v -= 0.5;
    }
    else if (action.rfind("retreat:", 0) == 0) {
        v += (ahp <= 60) ? 0.4 : -0.5;  // -0.5 penalty for healthy retreat
    }
    else if (action == "pass") {
        v -= 1.0;  // strongly discourage passing
    }

    int hs = (int)state.me.hand.size();
    if (hs >= 2 && dc > 10) v += 0.03 * std::min(hs, 5);

    return v;
}

std::vector<std::string> mask_illegal(const std::vector<std::string>& legal_actions, const BoardState& state) {
    if (legal_actions.empty()) return {"pass"};
    
    bool has_active_plays = false;
    for (const auto& action : legal_actions) {
        if (action != "pass") {
            if (action.rfind("attack:", 0) == 0 ||
                action.rfind("play_trainer:", 0) == 0 ||
                action.rfind("evolve:", 0) == 0 ||
                action.rfind("attach_energy:", 0) == 0 ||
                action.rfind("ability:", 0) == 0 ||
                action.rfind("bench:", 0) == 0) {
                
                if (action.rfind("play_trainer:", 0) == 0 && state.me.deck_count <= 0) {
                    std::string trainer_name = action.substr(13);
                    std::transform(trainer_name.begin(), trainer_name.end(), trainer_name.begin(), ::tolower);
                    if (trainer_name.find("research") != std::string::npos ||
                        trainer_name.find("iono") != std::string::npos ||
                        trainer_name.find("judge") != std::string::npos ||
                        trainer_name.find("draw") != std::string::npos) {
                        continue;
                    }
                }
                // Don't count impossible attacks as active plays
                if (action.rfind("attack:", 0) == 0) {
                    if (!state.me.has_active) continue;
                    int attached_count = (int)state.me.active.attached.size();
                    auto card = CardRegistry::getInstance().getCard(state.me.active.id);
                    int min_cost = (card && card->energy_cost > 0) ? card->energy_cost : 1;
                    if (attached_count < min_cost) continue;
                }
                has_active_plays = true;
                break;
            }
        }
    }

    std::vector<std::string> filtered;
    for (const auto& action : legal_actions) {
        if (action == "pass" && has_active_plays) {
            continue;
        }
        if (action.rfind("retreat:", 0) == 0 && state.me.bench.empty()) {
            continue;
        }
        if (action.rfind("play_trainer:", 0) == 0 && state.me.deck_count <= 0) {
            std::string trainer_name = action.substr(13);
            std::transform(trainer_name.begin(), trainer_name.end(), trainer_name.begin(), ::tolower);
            if (trainer_name.find("research") != std::string::npos ||
                trainer_name.find("iono") != std::string::npos ||
                trainer_name.find("judge") != std::string::npos ||
                trainer_name.find("draw") != std::string::npos) {
                continue;
            }
        }
        // Prune attacks when the active Pokemon lacks energy
        if (action.rfind("attack:", 0) == 0) {
            if (!state.me.has_active) continue;
            int attached_count = (int)state.me.active.attached.size();
            auto card = CardRegistry::getInstance().getCard(state.me.active.id);
            int min_cost = (card && card->energy_cost > 0) ? card->energy_cost : 1;
            if (attached_count < min_cost) continue;
        }
        filtered.push_back(action);
    }
    if (filtered.empty()) return {"pass"};
    return filtered;
}

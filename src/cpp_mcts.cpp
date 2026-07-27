#include "cpp_mcts.h"
#include "ptcg_simulator.h"
#include <chrono>
#include <algorithm>
#include <cmath>
#include <fstream>
#include <onnxruntime_cxx_api.h>

static Ort::Env* ort_env = nullptr;
static Ort::Session* ort_session = nullptr;

void init_onnx() {
    if (ort_session) return;
    try {
        ort_env = new Ort::Env(ORT_LOGGING_LEVEL_WARNING, "ptcg_core");
        Ort::SessionOptions session_options;
        session_options.SetIntraOpNumThreads(1);
        session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
        
        std::string model_path = "models/ppo_actor_critic.onnx";
        std::ifstream f(model_path.c_str());
        if (!f.good()) {
            model_path = "../models/ppo_actor_critic.onnx";
        }
        std::ifstream f2(model_path.c_str());
        if (!f2.good()) {
            model_path = "submission/models/ppo_actor_critic.onnx";
        }
        
        #ifdef _WIN32
        std::wstring w_model_path(model_path.begin(), model_path.end());
        ort_session = new Ort::Session(*ort_env, w_model_path.c_str(), session_options);
        #else
        ort_session = new Ort::Session(*ort_env, model_path.c_str(), session_options);
        #endif
    } catch (...) {
        ort_session = nullptr;
    }
}

void MASTPolicy::update(const std::vector<std::string>& actionsPlayed, bool won) {
    for (const auto& action : actionsPlayed) {
        action_visits[action]++;
        if (won) {
            action_wins[action]++;
        }
    }
}

double MASTPolicy::getActionPrior(const std::string& action) const {
    auto it = action_visits.find(action);
    if (it == action_visits.end() || it->second == 0) {
        return 0.5;
    }
    auto winIt = action_wins.find(action);
    double wins = (winIt != action_wins.end()) ? winIt->second : 0.0;
    return wins / it->second;
}

std::string MASTPolicy::selectRolloutAction(const std::vector<std::string>& legalActions, std::mt19937& rng) {
    if (legalActions.empty()) return "";
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    if (dist(rng) < exploration_weight) {
        std::uniform_int_distribution<size_t> idxDist(0, legalActions.size() - 1);
        return legalActions.at(idxDist(rng));
    }
    std::string bestAction = "";
    double bestRate = -1.0;
    for (const auto& action : legalActions) {
        double rate = 1.0;
        auto it = action_visits.find(action);
        if (it != action_visits.end() && it->second > 0) {
            auto winIt = action_wins.find(action);
            double wins = (winIt != action_wins.end()) ? winIt->second : 0.0;
            rate = wins / it->second;
        }
        if (rate > bestRate) {
            bestRate = rate;
            bestAction = action;
        }
    }
    if (bestAction.empty()) {
        std::uniform_int_distribution<size_t> idxDist(0, legalActions.size() - 1);
        return legalActions.at(idxDist(rng));
    }
    return bestAction;
}

void cpp_MCTSNode::expand(const std::vector<ActionPrior>& actionPriors) {
    std::vector<std::string> chance_actions = {"crushing_hammer", "pokemon_catcher", "super_scoop_up", "pokeball"};
    for (const auto& ap : actionPriors) {
        if (children.find(ap.action) == children.end()) {
            bool is_chance = false;
            std::string action_lower = ap.action;
            std::transform(action_lower.begin(), action_lower.end(), action_lower.begin(), ::tolower);
            for (const auto& ca : chance_actions) {
                if (action_lower.find(ca) != std::string::npos) {
                    is_chance = true;
                    break;
                }
            }
            if (is_chance) {
                auto chance_node = std::make_unique<cpp_MCTSNode>();
                chance_node->state_hash = state_hash + "_" + ap.action + "_chance";
                chance_node->parent = this;
                chance_node->action_taken = ap.action;
                chance_node->prior_prob = ap.prob;
                chance_node->is_chance_node = true;
                
                auto heads_node = std::make_unique<cpp_MCTSNode>();
                heads_node->state_hash = state_hash + "_" + ap.action + "_heads";
                heads_node->parent = chance_node.get();
                heads_node->action_taken = ap.action + "_heads";
                heads_node->prior_prob = 0.5;
                
                auto tails_node = std::make_unique<cpp_MCTSNode>();
                tails_node->state_hash = state_hash + "_" + ap.action + "_tails";
                tails_node->parent = chance_node.get();
                tails_node->action_taken = ap.action + "_tails";
                tails_node->prior_prob = 0.5;
                
                chance_node->children["heads"] = std::move(heads_node);
                chance_node->children["tails"] = std::move(tails_node);
                
                children[ap.action] = std::move(chance_node);
            } else {
                auto node = std::make_unique<cpp_MCTSNode>();
                node->state_hash = state_hash + "_" + ap.action;
                node->parent = this;
                node->action_taken = ap.action;
                node->prior_prob = ap.prob;
                children[ap.action] = std::move(node);
            }
        }
    }
}

std::string cpp_MCTSEngine::get_state_key(const BoardState& state) const {
    std::string key = std::to_string(state.turn_number) + "|";
    key += (state.turn_ended ? "T" : "F") + std::string("|");
    
    if (state.me.has_active) {
        key += "ma:" + state.me.active.id + ":" + std::to_string(state.me.active.hp) + ":";
        for (const auto& att : state.me.active.attached) {
            key += att + ",";
        }
        key += "|";
    } else {
        key += "ma:none|";
    }
    
    if (state.opponent.has_active) {
        key += "oa:" + state.opponent.active.id + ":" + std::to_string(state.opponent.active.hp) + ":";
        for (const auto& att : state.opponent.active.attached) {
            key += att + ",";
        }
        key += "|";
    } else {
        key += "oa:none|";
    }
    
    key += std::to_string(state.me.prizes) + ":" + std::to_string(state.opponent.prizes) + "|";
    
    key += "mh:";
    for (const auto& card : state.me.hand) {
        key += card + ",";
    }
    key += "|";
    
    key += "oh:" + std::to_string(state.opponent.hand.size()) + "|";
    
    key += "mb:";
    for (const auto& pkmn : state.me.bench) {
        key += pkmn.id + ":" + std::to_string(pkmn.hp) + ":";
        for (const auto& att : pkmn.attached) {
            key += att + ",";
        }
        key += ";";
    }
    key += "|";
    
    key += "ob:";
    for (const auto& pkmn : state.opponent.bench) {
        key += pkmn.id + ":" + std::to_string(pkmn.hp) + ":";
        for (const auto& att : pkmn.attached) {
            key += att + ",";
        }
        key += ";";
    }
    
    key += "|" + (state.me.supporter_played_this_turn ? std::string("S") : std::string("N"));
    
    return key;
}

std::vector<ActionPrior> cpp_MCTSEngine::get_action_priors(const BoardState& state, const std::vector<std::string>& legalActions, const MASTPolicy& mastPolicy) {
    std::vector<ActionPrior> priors;
    if (legalActions.empty()) return priors;
    
    for (const auto& a : legalActions) {
        // Query utility score from heuristic evaluator
        double score = score_action(a, state, 0.0);
        // Translate utility score to a positive prior weight (baseline 1.0 for neutral scores)
        double p = std::max(0.01, 1.0 + score);
        
        // Incorporate MAST (Move-Average Sampling Technique) feedback
        double mast_prior = mastPolicy.getActionPrior(a);
        p = 0.6 * p + 0.4 * mast_prior;
        
        priors.push_back({a, p});
    }
    
    // Normalize probabilities
    double total = 0.0;
    for (const auto& pr : priors) {
        total += pr.prob;
    }
    if (total > 0.0) {
        for (auto& pr : priors) {
            pr.prob /= total;
        }
    }
    return priors;
}

double cpp_MCTSEngine::evaluate_state(const BoardState& state, const std::string& action) {
    std::string key = get_state_key(state) + "_" + action;
    auto it = state_value_cache.find(key);
    if (it != state_value_cache.end()) {
        return it->second;
    }

    double value = 0.0;
    bool evaluated_by_onnx = false;

    if (state.game_over) {
        value = (state.winner == "me") ? 1.0 : -1.0;
        evaluated_by_onnx = true;
    } else {
        init_onnx();
        if (ort_session) {
            try {
                std::vector<int64_t> token_ids(32, 0);
                std::vector<int64_t> zone_ids(32, 0);
                std::vector<float> scalars(6, 0.0f);
                std::vector<uint8_t> padding_mask(33, 1); // 1 = padded/masked by default

                int idx = 0;
                // Fill hand
                for (const auto& card_id_str : state.me.hand) {
                    if (idx >= 32) break;
                    try {
                        token_ids[idx] = std::stoll(card_id_str);
                        zone_ids[idx] = 0; // hand
                        padding_mask[idx + 1] = 0;
                        idx++;
                    } catch(...) {}
                }
                // Fill active
                if (state.me.has_active && idx < 32) {
                    try {
                        token_ids[idx] = std::stoll(state.me.active.id);
                        zone_ids[idx] = 1; // active
                        padding_mask[idx + 1] = 0;
                        idx++;
                    } catch(...) {}
                }
                // Fill bench
                for (const auto& p : state.me.bench) {
                    if (idx >= 32) break;
                    try {
                        token_ids[idx] = std::stoll(p.id);
                        zone_ids[idx] = 2; // bench
                        padding_mask[idx + 1] = 0;
                        idx++;
                    } catch(...) {}
                }
                // Fill discard
                for (const auto& card_id_str : state.me.discard) {
                    if (idx >= 32) break;
                    try {
                        token_ids[idx] = std::stoll(card_id_str);
                        zone_ids[idx] = 3; // discard
                        padding_mask[idx + 1] = 0;
                        idx++;
                    } catch(...) {}
                }
                // CLS token (index 0) is never masked
                padding_mask[0] = 0;

                // Fill scalars
                scalars[0] = static_cast<float>(state.me.prizes);
                scalars[1] = static_cast<float>(state.opponent.prizes);
                scalars[2] = state.me.has_active ? static_cast<float>(state.me.active.hp) : 0.0f;
                scalars[3] = state.opponent.has_active ? static_cast<float>(state.opponent.active.hp) : 0.0f;
                scalars[4] = static_cast<float>(state.turn_number);
                scalars[5] = 0.0f; // weakness flag placeholder

                auto memory_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeCPU);
                
                std::vector<int64_t> token_shape = {1, 32};
                Ort::Value token_tensor = Ort::Value::CreateTensor<int64_t>(
                    memory_info, token_ids.data(), token_ids.size(), token_shape.data(), token_shape.size());
                
                std::vector<int64_t> zone_shape = {1, 32};
                Ort::Value zone_tensor = Ort::Value::CreateTensor<int64_t>(
                    memory_info, zone_ids.data(), zone_ids.size(), zone_shape.data(), zone_shape.size());
                
                std::vector<int64_t> scalars_shape = {1, 6};
                Ort::Value scalars_tensor = Ort::Value::CreateTensor<float>(
                    memory_info, scalars.data(), scalars.size(), scalars_shape.data(), scalars_shape.size());
                
                std::vector<int64_t> mask_shape = {1, 33};
                // ONNX Runtime expects bool tensors as bool/uint8/int8 array
                Ort::Value mask_tensor = Ort::Value::CreateTensor<bool>(
                    memory_info, reinterpret_cast<bool*>(padding_mask.data()), padding_mask.size(), mask_shape.data(), mask_shape.size());
                
                const char* input_names[] = {"token_ids", "zone_ids", "scalars", "padding_mask"};
                Ort::Value inputs[] = {std::move(token_tensor), std::move(zone_tensor), std::move(scalars_tensor), std::move(mask_tensor)};
                const char* output_names[] = {"logits", "value"};
                
                auto outputs = ort_session->Run(Ort::RunOptions{nullptr}, input_names, inputs, 4, output_names, 2);
                float* value_out = outputs[1].GetTensorMutableData<float>();
                value = static_cast<double>(value_out[0]);
                evaluated_by_onnx = true;
            } catch (...) {
                evaluated_by_onnx = false;
            }
        }
    }

    if (!evaluated_by_onnx) {
        value = score_state(state);
        double threat_penalty = state.opponent.hand.size() * 0.01;
        value += score_action(action, state, threat_penalty);
        
        std::uniform_real_distribution<double> dist(-0.01, 0.01);
        value += dist(rng);
    }
    
    double final_val = std::max(-1.0, std::min(1.0, value));
    state_value_cache[key] = final_val;
    return final_val;
}

cpp_MCTSNode* cpp_MCTSEngine::select_child(cpp_MCTSNode* node) {
    if (node->is_chance_node) {
        return sample_chance_child(node);
    }
    double bestScore = -1e9;
    cpp_MCTSNode* bestChild = nullptr;
    for (const auto& pair : node->children) {
        double score = calculate_ucb(pair.second.get(), node->visit_count);
        if (score > bestScore) {
            bestScore = score;
            bestChild = pair.second.get();
        }
    }
    if (!bestChild && !node->children.empty()) {
        bestChild = node->children.begin()->second.get();
    }
    return bestChild;
}

cpp_MCTSNode* cpp_MCTSEngine::sample_chance_child(cpp_MCTSNode* node) {
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    double r = dist(rng);
    double cumulative = 0.0;
    cpp_MCTSNode* last_child = nullptr;
    for (const auto& pair : node->children) {
        cumulative += pair.second->prior_prob;
        if (r <= cumulative) {
            return pair.second.get();
        }
        last_child = pair.second.get();
    }
    return last_child;
}

double cpp_MCTSEngine::calculate_ucb(const cpp_MCTSNode* child, int parentVisits) const {
    double q_value = child->get_q_value();
    double u_value = c_puct * child->prior_prob * std::sqrt(parentVisits) / (1.0 + child->visit_count);
    return q_value + u_value;
}

std::string cpp_MCTSEngine::search(const BoardState& rootState, double timeLimitSec, const std::unordered_map<std::string, double>& root_priors) {
    state_value_cache.clear();
    state_prior_cache.clear();

    std::vector<std::string> next_legal_actions = mask_illegal(rootState.legal_actions, rootState);
    if (next_legal_actions.empty()) return "pass";
    if (next_legal_actions.size() == 1) return next_legal_actions.at(0);
    
    // Prune redundant 'pass' if legal attacks or attachments are available
    bool has_active_plays = false;
    for (const auto& a : next_legal_actions) {
        if (a.rfind("attack", 0) == 0 || a.rfind("attach_energy", 0) == 0 || a.rfind("bench", 0) == 0 || a.rfind("evolve", 0) == 0) {
            has_active_plays = true;
            break;
        }
    }
    if (has_active_plays && next_legal_actions.size() > 1) {
        std::vector<std::string> pruned_actions;
        for (const auto& a : next_legal_actions) {
            if (a != "pass") pruned_actions.push_back(a);
        }
        if (!pruned_actions.empty()) {
            next_legal_actions = pruned_actions;
        }
    }
    if (next_legal_actions.size() == 1) return next_legal_actions.at(0);
    
    cpp_MCTSNode root;
    root.state_hash = "turn_" + std::to_string(rootState.turn_number);
    
    MASTPolicy mastPolicy(0.3);
    auto initial_priors = get_action_priors(rootState, next_legal_actions, mastPolicy);
    if (!root_priors.empty()) {
        for (auto& ap : initial_priors) {
            auto it = root_priors.find(ap.action);
            if (it != root_priors.end()) {
                ap.prob = it->second;
            }
        }
    }
    root.expand(initial_priors);
    
    auto startTime = std::chrono::steady_clock::now();
    
    // Cap maximum time limit at 0.75s to guarantee no Kaggle MCTS timeouts
    double effective_time_limit = std::min(timeLimitSec, 0.75);
    
    for (int sim = 0; sim < num_simulations; ++sim) {
        auto elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - startTime).count();
        if (elapsed >= effective_time_limit) {
            break;
        }
        
        BoardState current_gs = rootState;
        std::vector<cpp_MCTSNode*> path;
        path.push_back(&root);
        
        cpp_MCTSNode* node = select_child(&root);
        if (!node) continue;
        path.push_back(node);
        
        while (node->is_expanded()) {
            if (node->is_terminal) {
                break;
            }
            apply_action(current_gs, node->action_taken);
            cpp_MCTSNode* next_node = select_child(node);
            if (!next_node) break;
            node = next_node;
            path.push_back(node);
        }
        if (!node) continue;
        
        BoardState next_gs = current_gs;
        apply_action(next_gs, node->action_taken);
        
        double val = evaluate_state(next_gs, node->action_taken);
        
        if (next_gs.turn_ended || next_gs.game_over) {
            node->is_terminal = true;
        } else {
            std::string state_key = get_state_key(next_gs);
            auto prior_it = state_prior_cache.find(state_key);
            if (prior_it != state_prior_cache.end()) {
                node->expand(prior_it->second);
            } else {
                regenerate_legal_actions(next_gs);
                std::vector<std::string> canonical_next = mask_illegal(next_gs.legal_actions, next_gs);
                auto new_priors = get_action_priors(next_gs, canonical_next, mastPolicy);
                if (new_priors.empty() && canonical_next == std::vector<std::string>{"pass"}) {
                    new_priors.push_back({"pass", 1.0});
                }
                if (!new_priors.empty()) {
                    node->expand(new_priors);
                    state_prior_cache[state_key] = new_priors;
                }
            }
        }
        
        for (auto* n : path) {
            n->visit_count++;
            n->value_sum += val;
        }
        
        std::vector<std::string> actionsPlayed;
        for (auto* n : path) {
            if (!n->action_taken.empty()) {
                actionsPlayed.push_back(n->action_taken);
            }
        }
        mastPolicy.update(actionsPlayed, val > 0);
    }
    
    std::string bestAction = "";
    int maxVisits = -1;
    for (const auto& pair : root.children) {
        if (pair.second->visit_count > maxVisits) {
            maxVisits = pair.second->visit_count;
            bestAction = pair.first;
        }
    }
    if (bestAction.empty() && !next_legal_actions.empty()) {
        return next_legal_actions.at(0);
    }
    return bestAction;
}

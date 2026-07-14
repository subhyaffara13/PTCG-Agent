#ifndef CPP_MCTS_H
#define CPP_MCTS_H

#include "ptcg_types.h"
#include "ptcg_simulator.h"
#include <string>
#include <vector>
#include <unordered_map>
#include <memory>
#include <cmath>
#include <random>

struct ActionPrior {
    std::string action;
    double prob = 0.0;
};

class MASTPolicy {
public:
    MASTPolicy(double explorationWeight = 0.3) : exploration_weight(explorationWeight) {}

    void update(const std::vector<std::string>& actionsPlayed, bool won);
    double getActionPrior(const std::string& action) const;
    std::string selectRolloutAction(const std::vector<std::string>& legalActions, std::mt19937& rng);

private:
    std::unordered_map<std::string, int> action_wins;
    std::unordered_map<std::string, int> action_visits;
    double exploration_weight = 0.3;
};

struct cpp_MCTSNode {
    std::string state_hash;
    cpp_MCTSNode* parent = nullptr;
    std::string action_taken;
    double prior_prob = 1.0;
    bool is_chance_node = false;
    bool is_terminal = false;

    std::unordered_map<std::string, std::unique_ptr<cpp_MCTSNode>> children;
    std::vector<ActionPrior> unexpanded_priors;
    int visit_count = 0;
    double value_sum = 0.0;

    double get_q_value(double fpu_value = 0.0) const {
        if (visit_count == 0) return fpu_value;
        return value_sum / visit_count;
    }

    bool is_expanded() const {
        return !children.empty() || is_terminal;
    }

    void expand(const std::vector<ActionPrior>& actionPriors, int max_expand = -1);
};

class cpp_MCTSEngine {
public:
    cpp_MCTSEngine(double cPuct = 1.25, int numSimulations = 50)
        : c_puct(cPuct), num_simulations(numSimulations) {}

    std::string search(const BoardState& rootState, double timeLimitSec = 1.0, const std::unordered_map<std::string, double>& root_priors = {});
    void advance_root(const std::string& action);
    void reset_tree();

private:
    std::unique_ptr<cpp_MCTSNode> root;
    double c_puct = 1.25;
    int num_simulations = 50;
    std::mt19937 rng{std::random_device{}()};

    std::string get_state_key(const BoardState& state) const;
    std::unordered_map<std::string, double> state_value_cache;
    std::unordered_map<std::string, std::vector<ActionPrior>> state_prior_cache;

    std::vector<ActionPrior> get_action_priors(const BoardState& state, const std::vector<std::string>& legalActions, const MASTPolicy& mastPolicy);
    double evaluate_state(const BoardState& state, const std::string& action);
    cpp_MCTSNode* select_child(cpp_MCTSNode* node);
    cpp_MCTSNode* sample_chance_child(cpp_MCTSNode* node);
    double calculate_ucb(const cpp_MCTSNode* child, int parentVisits, double fpu_value) const;
};

#endif // CPP_MCTS_H

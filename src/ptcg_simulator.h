#ifndef PTCG_SIMULATOR_H
#define PTCG_SIMULATOR_H

#include "ptcg_types.h"
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cctype>

class CardRegistry {
public:
    static CardRegistry& getInstance() {
        static CardRegistry instance;
        return instance;
    }

    void loadFromFiles(const std::string& skillsDir);
    void addCard(const Card& card);
    const Card* getCard(const std::string& id) const;
    std::string getIdByName(const std::string& name) const;
    const std::unordered_map<std::string, Card>& getAllCards() const { return cards; }
    void clear() { cards.clear(); nameToId.clear(); }

private:
    CardRegistry() = default;
    std::unordered_map<std::string, Card> cards;
    std::unordered_map<std::string, std::string> nameToId;

    std::string lowercase(std::string s) const {
        std::transform(s.begin(), s.end(), s.begin(), [](unsigned char c){ return std::tolower(c); });
        return s;
    }
};

// Simulator transition functions
void apply_action(BoardState& state, const std::string& action);
void regenerate_legal_actions(BoardState& state);
void check_win_conditions(BoardState& state);
double score_state(const BoardState& state);
double score_action(const std::string& action, const BoardState& state, double threat_penalty);
std::vector<std::string> mask_illegal(const std::vector<std::string>& actions, const BoardState& state);

#endif // PTCG_SIMULATOR_H

#ifndef PTCG_SIMULATOR_INTERNAL_H_
#define PTCG_SIMULATOR_INTERNAL_H_

#include "ptcg_simulator.h"

// Function declarations (was static in original)
void remove_from_hand(std::vector<std::string>& hand, const std::string& card_id);
void draw_cards(BoardState& state, int n);
void apply_evolve(BoardState& state, const std::string& card_id);

#endif
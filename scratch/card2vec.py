import json
import logging
import os
import glob
from collections import Counter

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

logger = logging.getLogger(__name__)

class Card2Vec(nn.Module):
    def __init__(self, vocab_size, embedding_dim=64):
        super(Card2Vec, self).__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.out_layer = nn.Linear(embedding_dim, vocab_size, bias=False)
        
    def forward(self, center):
        emb = self.embeddings(center) # (batch_size, dim)
        out = self.out_layer(emb)     # (batch_size, vocab_size)
        return out

class SkipGramDataset(Dataset):
    def __init__(self, data):
        self.data = data
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        center, context = self.data[idx]
        return center, context

def generate_training_data(sentences, window_size=5):
    data = []
    for sentence in sentences:
        for i, target_word in enumerate(sentence):
            for j in range(max(0, i - window_size), min(len(sentence), i + window_size + 1)):
                if i != j:
                    data.append((target_word, sentence[j]))
    return data

def train_card2vec(corpus_decks, vocab_size, embedding_dim=64, epochs=5, batch_size=256, lr=0.01):
    """
    Trains a skip-gram model on the given corpus.
    corpus_decks: list of list of int (card indices mapped 0 to vocab_size-1).
    """
    data = generate_training_data(corpus_decks, window_size=5)
    if not data:
        logger.warning("No training data generated for Card2Vec.")
        return None
        
    dataset = SkipGramDataset(data)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    model = Card2Vec(vocab_size, embedding_dim)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for center, context in dataloader:
            optimizer.zero_grad()
            out = model(center) # out is (batch, vocab_size)
            loss = criterion(out, context)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        logger.info(f"Card2Vec Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")
        
    return model.embeddings.weight.data.cpu().numpy()

def load_winning_decks(logs_dir="logs"):
    """
    Parses logs to find winning decks. Returns a list of decks,
    where each deck is a list of card_ids.
    """
    decks = []
    
    # 1. Kaggle scraped decks
    kaggle_path = os.path.join(logs_dir, "kaggle_summary", "scraped_decks.json")
    if os.path.exists(kaggle_path):
        try:
            with open(kaggle_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if isinstance(item, dict) and "deck" in item:
                        # Assume deck is a list of card IDs, or list of dicts
                        deck_data = item["deck"]
                        parsed_deck = []
                        for c in deck_data:
                            if isinstance(c, dict) and "card_id" in c:
                                parsed_deck.extend([c["card_id"]] * c.get("count", 1))
                            elif isinstance(c, str):
                                parsed_deck.append(c) # Maybe card IDs are strings
                        if parsed_deck:
                            decks.append(parsed_deck)
        except Exception as e:
            logger.warning(f"Failed to load kaggle decks: {e}")
            
    # 2. Iteration results
    iter_path = os.path.join(logs_dir, "iteration_result.json")
    if os.path.exists(iter_path):
        try:
            with open(iter_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if isinstance(item, dict) and "deck" in item and item.get("win_rate", 0) > 0.5:
                        deck_data = item["deck"]
                        parsed_deck = []
                        for c in deck_data:
                            if isinstance(c, dict) and "card_id" in c:
                                parsed_deck.extend([c["card_id"]] * c.get("count", 1))
                            elif isinstance(c, str):
                                parsed_deck.append(c)
                        if parsed_deck:
                            decks.append(parsed_deck)
        except Exception as e:
            logger.warning(f"Failed to load iteration results: {e}")
            
    # 3. action_game_* files (from genetic optimizer and local training games)
    for filepath in glob.glob(os.path.join(logs_dir, "action_game_*.json")):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    winner = data.get("winner", "")
                    # Accept any of these winner identifiers for our agent's side
                    is_agent_win = (
                        winner == "agent"
                        or winner == "player_a"
                        or (isinstance(winner, str) and winner.startswith("opt_val_cand_"))
                    )
                    if is_agent_win:
                        # Try agent_deck first, then deck_a as fallback
                        raw_deck = data.get("agent_deck") or data.get("deck_a")
                        if raw_deck:
                            parsed_deck = []
                            for c in raw_deck:
                                if isinstance(c, dict) and "card_id" in c:
                                    parsed_deck.extend([c["card_id"]] * c.get("count", 1))
                                elif isinstance(c, (str, int)):
                                    parsed_deck.append(str(c))
                            if parsed_deck:
                                decks.append(parsed_deck)
        except Exception as e:
            logger.warning(f"Failed to parse {filepath}: {e}")
            
    return decks

class Card2VecTrainer:
    def __init__(self, vocab_cards):
        # vocab_cards is a list of all unique card_ids in the pool
        self.vocab = {c: i for i, c in enumerate(vocab_cards)}
        self.inverse_vocab = {i: c for c, i in self.vocab.items()}
        self.embedding_matrix = None
        
    def train(self, logs_dir="logs", embedding_dim=64, epochs=5):
        raw_decks = load_winning_decks(logs_dir)
        
        # Convert to indices
        corpus_indices = []
        for deck in raw_decks:
            idx_deck = [self.vocab[c] for c in deck if c in self.vocab]
            if idx_deck:
                corpus_indices.append(idx_deck)
                
        if not corpus_indices:
            logger.warning("No valid decks found for Card2Vec training.")
            return False
            
        self.embedding_matrix = train_card2vec(
            corpus_indices, 
            vocab_size=len(self.vocab), 
            embedding_dim=embedding_dim, 
            epochs=epochs
        )
        return self.embedding_matrix is not None

    def get_embedding(self, card_id):
        if self.embedding_matrix is not None and card_id in self.vocab:
            idx = self.vocab[card_id]
            return self.embedding_matrix[idx]
        return None

import logging
import random
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from scratch.deck_builder import make_deck
from scratch.deck_simulator import evaluate_single_candidate
from scratch.deck_surrogate_model import DeckFitnessMLP, _build_card_index, _deck_to_tensor, _max_copies_tensor
from scratch.deck_surrogate_train_parts import decode_continuous as _decode_continuous, optimize_via_surrogate
from scratch.deck_embedding_utils import build_embedding_index

logger = logging.getLogger(__name__)


def build_training_data(pool_cards, details, scores, pokemon_pool, basics, energy_pool, trainer_pool, n_samples=500):
    data = []
    for _ in range(n_samples):
        limit = max(1, len(pokemon_pool) // 2)
        p_lines = random.sample(pokemon_pool[:limit], min(len(pokemon_pool), random.randint(1, 3)))
        deck = make_deck(p_lines, trainer_pool, energy_pool, basics, pool_cards, details)
        if len(deck) == 60:
            try:
                data.append((deck, evaluate_single_candidate((deck, scores, details))))
            except Exception as e:
                logger.warning("Failed to evaluate deck: %s", e)
    return data


def train_surrogate_model(pool_cards, details, scores, training_data, epochs=150):
    cards, card_index = _build_card_index(pool_cards)
    _, embeddings_np = build_embedding_index(cards, details)
    embeddings_t = torch.tensor(embeddings_np, dtype=torch.float32)
    
    N, max_cp = len(cards), _max_copies_tensor(cards)
    X, y = [], []
    for deck, fitness in training_data:
        counts = _deck_to_tensor(deck, card_index, N) / max_cp
        deck_feature = torch.matmul(counts, embeddings_t)
        X.append(deck_feature)
        y.append(fitness)
    X, y = torch.stack(X), torch.tensor(y, dtype=torch.float32)
    split = int(len(X) * 0.8)
    train_loader = DataLoader(TensorDataset(X[:split], y[:split]), batch_size=32, shuffle=True)
    val_loader = DataLoader(TensorDataset(X[split:], y[split:]), batch_size=32, shuffle=False)
    model = DeckFitnessMLP(embeddings_t.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, patience=10)
    best_val = float("inf")
    for epoch in range(epochs):
        model.train()
        for batch_x, batch_y in train_loader:
            opt.zero_grad()
            F.mse_loss(model(batch_x), batch_y).backward()
            opt.step()
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                val_loss += F.mse_loss(model(batch_x), batch_y, reduction="sum").item()
        val_loss /= len(val_loader.dataset)
        sched.step(val_loss)
        if val_loss < best_val:
            best_val = val_loss
    logger.info("Training complete, best val loss: %.4f", best_val)
    return model, cards, card_index, max_cp, embeddings_t

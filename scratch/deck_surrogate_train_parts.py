"""Helper functions extracted from deck_surrogate_train.py."""

import logging
import torch
import torch.nn.functional as F
from scratch.deck_milp import optimize_deck_milp

logger = logging.getLogger(__name__)


def decode_continuous(logits, cards, max_cp, target_size=60):
    raw = torch.sigmoid(logits) * max_cp
    counts = torch.round(raw).int()
    mc = max_cp.int()
    counts = torch.where(counts < 0, torch.zeros_like(counts), counts)
    counts = torch.where(counts > mc, mc, counts)
    total = counts.sum().item()
    if total != target_size:
        need = target_size - total
        sign = 1 if need > 0 else -1
        diff = (raw - counts.float()) * sign
        for idx in diff.argsort(descending=True):
            if need == 0:
                break
            can = (sign > 0 and counts[idx] < int(mc[idx].item())) or (sign < 0 and counts[idx] > 0)
            if can:
                counts[idx] += sign
                need -= sign
    deck = []
    for i, c in enumerate(cards):
        cnt = int(counts[i].item())
        if cnt > 0:
            deck.extend([c] * cnt)
    return deck


def optimize_via_surrogate(model, cards, card_index, max_cp, embeddings_t, pool_cards, details, scores, steps=500, lr=0.05):
    N = len(cards)
    logits = torch.randn(N, requires_grad=True)
    opt = torch.optim.Adam([logits], lr=lr)
    masks = {t: torch.tensor([1.0 if c.get("card_type") == t else 0.0 for c in cards]) for t in ("Pokemon", "Trainer", "Energy")}
    with torch.no_grad():
        dummy_feature = torch.matmul((torch.sigmoid(logits) * max_cp / max_cp).unsqueeze(0), embeddings_t)
        PRED_SCALE = max(1.0, model(dummy_feature).abs().mean().item())
    for _ in range(steps):
        opt.zero_grad()
        x = torch.sigmoid(logits) * max_cp
        deck_feature = torch.matmul((x / max_cp).unsqueeze(0), embeddings_t)
        pred = model(deck_feature)
        total, pk, tr, en = x.sum(), (x * masks["Pokemon"]).sum(), (x * masks["Trainer"]).sum(), (x * masks["Energy"]).sum()
        penalty = ((total - 60) ** 2 + F.relu(10 - pk) ** 2 + F.relu(pk - 20) ** 2 + F.relu(25 - tr) ** 2 + F.relu(8 - en) ** 2 + F.relu(en - 16) ** 2)
        loss = -pred.mean() / PRED_SCALE + 50.0 * penalty + 0.01 * logits.abs().mean()
        loss.backward()
        opt.step()
    deck = decode_continuous(logits.detach(), cards, max_cp)
    try:
        milp_fixed = optimize_deck_milp(deck, pool_cards, details, scores)
        if len(milp_fixed) == 60:
            return milp_fixed
    except Exception as e:
        logger.warning("MILP optimization failed: %s", e)
    return deck[:60]

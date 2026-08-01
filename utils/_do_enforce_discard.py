
def _do_enforce_discard(self, legal, pool, deck, copies, ctr):
    import random
    src = [c for c in legal if "discard" in c.get("combo_tags", [])] or [c for c in pool if "discard" in c.get("combo_tags", [])]
    for _ in range(100):
        if ctr["discard"] >= 2 or not src: break
        self.add_card(random.choice(src), 1, deck, copies, ctr)



def _do_enforce_supporters(self, legal, pool, deck, copies, ctr):
    import random
    sp = [c for c in legal if self.is_supporter(c)] or [c for c in pool if self.is_supporter(c)]
    for _ in range(100):
        if ctr["supporter"] >= 8 or not sp: break
        self.add_card(random.choice(sp), 2, deck, copies, ctr)


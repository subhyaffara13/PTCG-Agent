class DeckInjectionMixin:
    def add_card(self, card: dict, count: int, deck: list, copies: dict, ctr: dict) -> int:
        cid = str(card["card_id"])
        mx = 99 if card.get("card_type") == "Energy" and "Basic" in card.get("card_name", "") else 4
        added = 0
        for _ in range(count):
            if len(deck) < 60 and copies.get(cid, 0) < mx:
                deck.append(dict(card)); copies[cid] = copies.get(cid, 0) + 1; added += 1
                ct = card.get("card_type")
                if ct == "Pokemon": ctr["pkmn"] += 1
                elif ct == "Energy": ctr["energy"] += 1
                if self.is_supporter(card): ctr["supporter"] += 1
                if "discard" in card.get("combo_tags", []): ctr["discard"] += 1
        return added

    def inject_signature_cards(self, arch, id_map, name_map, deck, copies, ctr):
        import random
        sig_pool = arch.get("signature_cards", [])
        if sig_pool:
            # Pick a core focus rather than mixing 10 different archetypes
            focus = random.sample(sig_pool, min(len(sig_pool), random.randint(1, 2)))
        else:
            focus = []
            
        for sid in focus:
            s = str(sid)
            if s in id_map: self.add_card(id_map[s], 4, deck, copies, ctr)
            elif s.lower() in name_map: self.add_card(name_map[s.lower()], 4, deck, copies, ctr)
            
        # Optional: pull some from the card pool if there's room, but don't force all of them
        c_pool = arch.get("card_pool", [])
        if c_pool:
            supp_focus = random.sample(c_pool, min(len(c_pool), 2))
            for sid in supp_focus:
                s = str(sid)
                if s in id_map: self.add_card(id_map[s], 2, deck, copies, ctr)
                elif s.lower() in name_map: self.add_card(name_map[s.lower()], 2, deck, copies, ctr)

    def inject_evolution_pyramids(self, deck, details, name_map, copies, ctr):
        # Build forward evolution maps: basic_name -> [stage1_cards], stage1_name -> [stage2_cards]
        fwd_s1 = {}
        fwd_s2 = {}
        for cid, det in details.items():
            prev = det.get("previous_stage")
            if prev:
                stage = det.get("stage")
                prev_lower = prev.lower()
                if stage == "Stage 1":
                    fwd_s1.setdefault(prev_lower, []).append(cid)
                elif stage == "Stage 2":
                    s1_name = prev_lower
                    fwd_s2.setdefault(s1_name, []).append(cid)
        
        processed = set()
        for pkmn in [c for c in deck if c.get("card_type") == "Pokemon"]:
            det = details.get(str(pkmn["card_id"]), {})
            stage = det.get("stage")
            pkmn_name_lower = det.get("card_name", "").lower()
            if pkmn_name_lower in processed:
                continue
            processed.add(pkmn_name_lower)
            
            if stage == "Basic":
                # Forward: Basic (4x) -> add Stage 1 (3x) and Stage 2 (2x)
                self.add_card(pkmn, 4, deck, copies, ctr)
                s1_ids = fwd_s1.get(pkmn_name_lower, [])
                for s1_id in s1_ids:
                    if s1_id in name_map:
                        self.add_card(name_map[s1_id], 3, deck, copies, ctr)
                        s1_name = details.get(s1_id, {}).get("card_name", "").lower()
                        if s1_name:
                            processed.add(s1_name)
                        s2_ids = fwd_s2.get(s1_id, []) or fwd_s2.get(s1_name, [])
                        for s2_id in s2_ids:
                            if s2_id in name_map:
                                self.add_card(name_map[s2_id], 2, deck, copies, ctr)
                                s2_name = details.get(s2_id, {}).get("card_name", "").lower()
                                if s2_name:
                                    processed.add(s2_name)
            elif stage == "Stage 1":
                # Backward: add Basic (4x), forward: add Stage 2 (2x)
                p0 = det.get("previous_stage")
                if p0 and p0.lower() in name_map:
                    self.add_card(name_map[p0.lower()], 4, deck, copies, ctr)
                    processed.add(p0.lower())
                self.add_card(pkmn, 3, deck, copies, ctr)
                s2_ids = fwd_s2.get(str(pkmn["card_id"]), []) or fwd_s2.get(pkmn_name_lower, [])
                for s2_id in s2_ids:
                    if s2_id in name_map:
                        self.add_card(name_map[s2_id], 2, deck, copies, ctr)
                        s2_name = details.get(s2_id, {}).get("card_name", "").lower()
                        if s2_name:
                            processed.add(s2_name)
            elif stage == "Stage 2":
                # Backward: add Basic (4x) and Stage 1 (3x), Stage 2 (2x)
                self.add_card(pkmn, 2, deck, copies, ctr)
                p1 = det.get("previous_stage")
                if p1 and p1.lower() in name_map:
                    self.add_card(name_map[p1.lower()], 3, deck, copies, ctr)
                    processed.add(p1.lower())
                    p0 = details.get(str(name_map[p1.lower()]["card_id"]), {}).get("previous_stage")
                    if p0 and p0.lower() in name_map:
                        self.add_card(name_map[p0.lower()], 4, deck, copies, ctr)
                        processed.add(p0.lower())

    def inject_consistency_trainers(self, deck, details, id_map, name_map, copies, ctr):
        ids = {"1121": 4, "ultra-ball-sv1-196": 4, "nest-ball-sv1-255": 4,
               "1102": 4, "professor-s-research-sv1-190": 4, "1086": 4, "iono-pal-185": 4, "1213": 4}
        names = {"ultra ball": 4, "nest ball": 4, "professor's research": 4,
                 "iono": 4, "switch": 2, "boss's orders": 2}
        if any(details.get(str(c["card_id"]), {}).get("stage") == "Stage 2"
               for c in deck if c.get("card_type") == "Pokemon"):
            ids.update({"rare-candy-sv1-191": 4, "1079": 4})
        for tid, tc in ids.items():
            if tid in id_map: self.add_card(id_map[tid], tc, deck, copies, ctr)
        for tn, tc in names.items():
            if tn in name_map: self.add_card(name_map[tn], tc, deck, copies, ctr)

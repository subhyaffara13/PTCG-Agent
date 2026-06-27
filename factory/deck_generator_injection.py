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
        for sid in arch.get("signature_cards", []) + arch.get("card_pool", []):
            s = str(sid)
            if s in id_map: self.add_card(id_map[s], 2, deck, copies, ctr)
            elif s.lower() in name_map: self.add_card(name_map[s.lower()], 2, deck, copies, ctr)

    def inject_evolution_pyramids(self, deck, details, name_map, copies, ctr):
        for pkmn in [c for c in deck if c.get("card_type") == "Pokemon"]:
            det = details.get(str(pkmn["card_id"]), {})
            if det.get("stage") == "Stage 2":
                p1 = det.get("previous_stage")
                if p1 and p1.lower() in name_map:
                    self.add_card(name_map[p1.lower()], 3, deck, copies, ctr)
                    p0 = details.get(str(name_map[p1.lower()]["card_id"]), {}).get("previous_stage")
                    if p0 and p0.lower() in name_map: self.add_card(name_map[p0.lower()], 4, deck, copies, ctr)
            elif det.get("stage") == "Stage 1":
                p0 = det.get("previous_stage")
                if p0 and p0.lower() in name_map: self.add_card(name_map[p0.lower()], 4, deck, copies, ctr)

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

function renderPlayerBoard(playerData, handDOM, benchDOM, activeDOM, prizesDOM, deckDOM, pClass) {
    if (!playerData) return;

    handDOM.innerHTML = "";
    const hand = playerData.hand || [];
    hand.forEach(card => {
        const cardId = card.id || card;
        const details = getCardDetails(cardId);
        const cardDiv = document.createElement("div");
        cardDiv.className = `card-item ${details.type}`;
        if (pClass.includes("opp")) {
            cardDiv.innerHTML = `
                <div class="card-image" style="background-color: #1a237e; border-radius: 6px; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; min-height: 120px;">?</div>
            `;
        } else {
            cardDiv.innerHTML = `
                <img src="images/card_${cardId}.jpeg" alt="${details.name}" class="card-image" onerror="this.style.opacity='0.2';">
            `;
        }
        handDOM.appendChild(cardDiv);
    });

    benchDOM.innerHTML = "";
    const bench = playerData.bench || [];
    bench.forEach(pokemon => {
        if (!pokemon) return;
        const cardId = pokemon.id || pokemon;
        const details = getCardDetails(cardId);
        const cardDiv = document.createElement("div");
        cardDiv.className = `card-item pokemon`;
        cardDiv.style.position = "relative";

        let energiesHtml = "";
        if (pokemon.energyCards && pokemon.energyCards.length > 0) {
            energiesHtml = '<div style="position: absolute; bottom: 2px; left: 2px; display: flex; z-index: 10;">';
            pokemon.energyCards.forEach(eCard => {
                const eId = eCard.id || eCard;
                energiesHtml += `<img src="images/card_${eId}.jpeg" style="width: 18px; height: 18px; border-radius: 50%; border: 1px solid white; margin-right: -8px; box-shadow: 0px 1px 3px rgba(0,0,0,0.8);" onerror="this.style.opacity='0.2';">`;
            });
            energiesHtml += '</div>';
        }

        cardDiv.innerHTML = `
            <img src="images/card_${cardId}.jpeg" alt="${details.name}" class="card-image" onerror="this.style.opacity='0.2';">
            ${energiesHtml}
        `;
        benchDOM.appendChild(cardDiv);
    });

    activeDOM.innerHTML = "";
    const activeList = playerData.active || [];
    if (activeList.length > 0 && activeList[0]) {
        const active = activeList[0];
        const cardId = active.id || active;
        const details = getCardDetails(cardId);
        const hpPercent = Math.max(0, Math.min(100, ((active.hp || 100) / (active.maxHp || 100)) * 100));

        let energiesHtml = "";
        if (active.energyCards && active.energyCards.length > 0) {
            energiesHtml = '<div style="position: absolute; bottom: 5px; left: 5px; display: flex; z-index: 10;">';
            active.energyCards.forEach(eCard => {
                const eId = eCard.id || eCard;
                energiesHtml += `<img src="images/card_${eId}.jpeg" style="width: 24px; height: 24px; border-radius: 50%; border: 1px solid white; margin-right: -10px; box-shadow: 0px 1px 4px rgba(0,0,0,0.8);" onerror="this.style.opacity='0.2';">`;
            });
            energiesHtml += '</div>';
        }

        activeDOM.innerHTML = `
            <div class="active-pokemon-card ${pClass}" style="position: relative;">
                <img src="images/card_${cardId}.jpeg" alt="${details.name}" class="active-card-image" onerror="this.style.opacity='0.2';">
                <div class="active-overlay">
                    <div style="font-size: 0.8rem; font-weight: bold; color: var(--text-primary);">HP: ${active.hp || 100}/${active.maxHp || 100}</div>
                    <div class="active-hp-bar">
                        <div class="active-hp-inner" style="width: ${hpPercent}%"></div>
                    </div>
                </div>
                ${energiesHtml}
            </div>
        `;
    } else {
        activeDOM.innerHTML = `<div style="color: var(--text-secondary); font-size: 0.85rem">Empty Active Slot</div>`;
    }

    const prizeCount = Array.isArray(playerData.prize) ? playerData.prize.length : 6;
    prizesDOM.textContent = 6 - prizeCount;

    deckDOM.textContent = playerData.deckCount !== undefined ? playerData.deckCount : 60;
}

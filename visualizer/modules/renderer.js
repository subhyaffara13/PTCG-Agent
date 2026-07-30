function renderStep(idx) {
    currentStepTxt.textContent = idx;
    const stepData = gameSteps[idx];
    if (!stepData) return;

    const p1State = stepData.players[0];
    const p2State = stepData.players[1];

    if (p1State && p1State.observation) {
        const current = p1State.observation.current || {};
        currentTurnTxt.textContent = current.turn || 1;
        gamePhaseTxt.textContent = stepData.players[0].status || "NORMAL";

        const players = current.players || [];
        if (players.length > 0) {
            renderPlayerBoard(players[0], p1Hand, p1Bench, p1Active, p1Prizes, p1Deck, "p1");
        }
        if (players.length > 1) {
            renderPlayerBoard(players[1], p2Hand, p2Bench, p2Active, p2Prizes, p2Deck, "p2");
        }
    }

    rebuildLogs(idx);
}

function rebuildLogs(maxIdx) {
    logOutput.innerHTML = "";
    for (let i = 0; i <= maxIdx; i++) {
        const stepData = gameSteps[i];
        if (!stepData) continue;

        if (i === 0) {
            const entry = document.createElement("div");
            entry.className = "log-entry turn-header";
            entry.textContent = "Game Started";
            logOutput.appendChild(entry);
        }

        const logsList = [];
        stepData.players.forEach(p => {
            if (p.action !== null && p.action !== undefined) {
                const actionStr = Array.isArray(p.action) ? p.action.join(", ") : p.action;
                logsList.push(`Player ${p.player + 1} chose option indices: [${actionStr}]`);
            }
        });

        if (logsList.length > 0) {
            const logItem = document.createElement("div");
            logItem.className = "log-entry";
            logItem.innerHTML = `<strong>Step ${i}:</strong><br>${logsList.join("<br>")}`;
            logOutput.appendChild(logItem);
        }
    }
    logOutput.scrollTop = logOutput.scrollHeight;
}

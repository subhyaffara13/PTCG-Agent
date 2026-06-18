// Card name database lookup
const CARD_DATABASE = {
    721: { name: "Pikachu", type: "pokemon" },
    722: { name: "Raichu", type: "pokemon" },
    723: { name: "Magnemite", type: "pokemon" },
    1092: { name: "Professor's Research", type: "trainer" },
    1121: { name: "Poké Ball", type: "trainer" },
    1145: { name: "Switch", type: "trainer" },
    1163: { name: "Potion", type: "trainer" },
    1219: { name: "Great Ball", type: "trainer" },
    1227: { name: "Ultra Ball", type: "trainer" },
    1262: { name: "Nest Ball", type: "trainer" },
    3: { name: "Energy", type: "energy" }
};

function getCardDetails(cardId) {
    if (CARD_DATABASE[cardId]) {
        return CARD_DATABASE[cardId];
    }
    return { name: `Card #${cardId}`, type: "trainer" };
}

// Playback state variables
let gameSteps = [];
let currentStepIdx = 0;
let playbackInterval = null;
let playbackSpeedMs = 1000;

// UI Elements
const fileInput = document.getElementById("game-file-input");
const btnPrev = document.getElementById("btn-prev");
const btnPlay = document.getElementById("btn-play");
const btnNext = document.getElementById("btn-next");
const speedRange = document.getElementById("speed-range");
const speedVal = document.getElementById("speed-val");
const timelineSlider = document.getElementById("timeline-slider");

const currentStepTxt = document.getElementById("current-step");
const totalStepsTxt = document.getElementById("total-steps");
const currentTurnTxt = document.getElementById("current-turn");
const gamePhaseTxt = document.getElementById("game-phase");
const logOutput = document.getElementById("log-output");

// Player 1 DOM elements
const p1Hand = document.getElementById("player-hand");
const p1Bench = document.getElementById("player-bench");
const p1Active = document.getElementById("player-active");
const p1Prizes = document.getElementById("player-prizes");
const p1Deck = document.getElementById("player-deck");

// Player 2 DOM elements
const p2Hand = document.getElementById("opp-hand");
const p2Bench = document.getElementById("opp-bench");
const p2Active = document.getElementById("opp-active");
const p2Prizes = document.getElementById("opp-prizes");
const p2Deck = document.getElementById("opp-deck");

// Handle File upload
fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            gameSteps = JSON.parse(e.target.result);
            currentStepIdx = 0;
            initPlayback();
        } catch (err) {
            alert("Failed to parse JSON file: " + err.message);
        }
    };
    reader.readAsText(file);
});

function initPlayback() {
    if (gameSteps.length === 0) return;
    
    totalStepsTxt.textContent = gameSteps.length - 1;
    timelineSlider.max = gameSteps.length - 1;
    timelineSlider.value = 0;
    
    // Enable/disable navigation buttons
    btnNext.disabled = gameSteps.length <= 1;
    btnPrev.disabled = true;

    renderStep(0);
}

// Navigation triggers
btnPrev.addEventListener("click", () => {
    if (currentStepIdx > 0) {
        currentStepIdx--;
        updateTimeline();
        renderStep(currentStepIdx);
    }
});

btnNext.addEventListener("click", () => {
    if (currentStepIdx < gameSteps.length - 1) {
        currentStepIdx++;
        updateTimeline();
        renderStep(currentStepIdx);
    }
});

timelineSlider.addEventListener("input", (e) => {
    currentStepIdx = parseInt(e.target.value);
    renderStep(currentStepIdx);
    updateTimelineControls();
});

btnPlay.addEventListener("click", () => {
    if (playbackInterval) {
        pause();
    } else {
        play();
    }
});

speedRange.addEventListener("input", (e) => {
    playbackSpeedMs = parseFloat(e.target.value) * 1000;
    speedVal.textContent = e.target.value + "s";
    if (playbackInterval) {
        pause();
        play();
    }
});

function play() {
    btnPlay.textContent = "Pause";
    playbackInterval = setInterval(() => {
        if (currentStepIdx < gameSteps.length - 1) {
            currentStepIdx++;
            updateTimeline();
            renderStep(currentStepIdx);
        } else {
            pause();
        }
    }, playbackSpeedMs);
}

function pause() {
    btnPlay.textContent = "Play";
    clearInterval(playbackInterval);
    playbackInterval = null;
}

function updateTimeline() {
    timelineSlider.value = currentStepIdx;
    updateTimelineControls();
}

function updateTimelineControls() {
    btnPrev.disabled = currentStepIdx === 0;
    btnNext.disabled = currentStepIdx === gameSteps.length - 1;
}

// Main Render Function
function renderStep(idx) {
    currentStepTxt.textContent = idx;
    const stepData = gameSteps[idx];
    if (!stepData) return;

    // We take Player 0 as Player 1 (Candidate) and Player 1 as Player 2 (Opponent)
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

    // Render step action logs
    appendLog(idx, stepData);
}

function renderPlayerBoard(playerData, handDOM, benchDOM, activeDOM, prizesDOM, deckDOM, pClass) {
    if (!playerData) return;

    // 1. Hand
    handDOM.innerHTML = "";
    const hand = playerData.hand || [];
    hand.forEach(card => {
        const details = getCardDetails(card.id || card);
        const cardDiv = document.createElement("div");
        cardDiv.className = `card-item ${details.type}`;
        cardDiv.innerHTML = `
            <div class="card-name">${details.name}</div>
            <div class="card-type-lbl">${details.type}</div>
        `;
        handDOM.appendChild(cardDiv);
    });

    // 2. Bench
    benchDOM.innerHTML = "";
    const bench = playerData.bench || [];
    bench.forEach(pokemon => {
        if (!pokemon) return;
        const details = getCardDetails(pokemon.id || pokemon);
        const cardDiv = document.createElement("div");
        cardDiv.className = `card-item pokemon`;
        cardDiv.innerHTML = `
            <div class="card-name">${details.name}</div>
            <div class="card-type-lbl">Bench (HP: ${pokemon.hp || 100})</div>
        `;
        benchDOM.appendChild(cardDiv);
    });

    // 3. Active Pokémon
    activeDOM.innerHTML = "";
    const activeList = playerData.active || [];
    if (activeList.length > 0 && activeList[0]) {
        const active = activeList[0];
        const details = getCardDetails(active.id || active);
        const hpPercent = Math.max(0, Math.min(100, ((active.hp || 100) / (active.maxHp || 100)) * 100));
        activeDOM.innerHTML = `
            <div class="active-pokemon-card ${pClass}">
                <div>
                    <h3 style="font-size: 1.1rem; font-family: 'Space Grotesk'">${details.name}</h3>
                    <div style="font-size: 0.8rem; opacity: 0.8">HP: ${active.hp || 100}/${active.maxHp || 100}</div>
                    <div class="active-hp-bar">
                        <div class="active-hp-inner" style="width: ${hpPercent}%"></div>
                    </div>
                </div>
                <div style="font-size: 0.8rem; text-transform: uppercase; font-weight: bold; opacity: 0.6">Active Spot</div>
            </div>
        `;
    } else {
        activeDOM.innerHTML = `<div style="color: var(--text-secondary); font-size: 0.85rem">Empty Active Slot</div>`;
    }

    // 4. Prizes Remaining
    const prizeCount = Array.isArray(playerData.prize) ? playerData.prize.length : 6;
    prizesDOM.textContent = 6 - prizeCount;

    // 5. Deck count
    deckDOM.textContent = playerData.deckCount !== undefined ? playerData.deckCount : 60;
}

function appendLog(idx, stepData) {
    if (idx === 0) {
        logOutput.innerHTML = `<div class="log-entry turn-header">Game Started</div>`;
    }

    const logsList = [];
    stepData.players.forEach(p => {
        if (p.action !== null && p.action !== undefined) {
            logsList.push(`Player ${p.player + 1} chose option indices: [${p.action.join(", ")}]`);
        }
    });

    if (logsList.length > 0) {
        const logItem = document.createElement("div");
        logItem.className = "log-entry";
        logItem.innerHTML = `<strong>Step ${idx}:</strong><br>${logsList.join("<br>")}`;
        logOutput.appendChild(logItem);
        logOutput.scrollTop = logOutput.scrollHeight;
    }
}

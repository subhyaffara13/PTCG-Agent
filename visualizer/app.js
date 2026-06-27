const CARD_DATABASE = {
    721: { name: "Kyogre", type: "pokemon" },
    722: { name: "Snover", type: "pokemon" },
    723: { name: "Mega Abomasnow ex", type: "pokemon" },
    1092: { name: "Professor's Research", type: "trainer" },
    1121: { name: "Poké Ball", type: "trainer" },
    1145: { name: "Switch", type: "trainer" },
    1163: { name: "Potion", type: "trainer" },
    1219: { name: "Great Ball", type: "trainer" },
    1227: { name: "Ultra Ball", type: "trainer" },
    1262: { name: "Nest Ball", type: "trainer" },
    3: { name: "Basic {W} Energy", type: "energy" }
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

const fileSelect = document.getElementById("game-file-select");

// Populate files list from /data/ listing page
async function loadAvailableLogs() {
    try {
        if (window.location.protocol === 'file:') {
            fileSelect.innerHTML = `<option value="">Use http://localhost:8000 to see options</option>`;
            console.warn("Visualizer opened via file:// protocol. Local logs list is only available when served over HTTP (http://localhost:8000).");
            return;
        }

        const response = await fetch('/data/');
        if (!response.ok) {
            fileSelect.innerHTML = `<option value="">Failed to fetch log options</option>`;
            return;
        }
        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const files = Array.from(doc.querySelectorAll('a'))
            .map(a => a.getAttribute('href'))
            .filter(href => href && href.endsWith('.json'))
            .map(href => decodeURIComponent(href.split('/').pop()));

        const uniqueFiles = Array.from(new Set(files)).sort().reverse();

        if (uniqueFiles.length > 0) {
            fileSelect.innerHTML = `<option value="">-- Select Match Log --</option>`;
            uniqueFiles.forEach(file => {
                const opt = document.createElement("option");
                opt.value = file;
                
                // Determine friendly nickname
                let nickname = file;
                const match = file.match(/iter_(\d+)_(reasoning_test|deck_test|variance_baseline)\.json/);
                if (match) {
                    const iterNum = match[1];
                    const testType = match[2];
                    let label = "";
                    if (testType === "reasoning_test") {
                        label = "Logic Staging (New vs Old)";
                    } else if (testType === "deck_test") {
                        label = "Deck Staging (New vs Old)";
                    } else if (testType === "variance_baseline") {
                        label = "RNG / Noise Control Match";
                    }
                    nickname = `Iteration ${iterNum} — ${label}`;
                }
                
                opt.textContent = nickname;
                fileSelect.appendChild(opt);
            });
        } else {
            fileSelect.innerHTML = `<option value="">No log files found in data/</option>`;
        }
    } catch (err) {
        console.error("Failed to load available logs:", err);
        fileSelect.innerHTML = `<option value="">Error loading logs list</option>`;
    }
}

// Handle select change
fileSelect.addEventListener("change", async (event) => {
    const filename = event.target.value;
    if (!filename) return;

    try {
        const response = await fetch(`/data/${encodeURIComponent(filename)}`);
        if (!response.ok) throw new Error("Server returned status " + response.status);
        gameSteps = await response.json();
        currentStepIdx = 0;
        initPlayback();
    } catch (err) {
        alert("Failed to load match JSON: " + err.message);
    }
});

// Call on startup
loadAvailableLogs();

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
    rebuildLogs(idx);
}

function renderPlayerBoard(playerData, handDOM, benchDOM, activeDOM, prizesDOM, deckDOM, pClass) {
    if (!playerData) return;

    // 1. Hand
    handDOM.innerHTML = "";
    const hand = playerData.hand || [];
    hand.forEach(card => {
        const cardId = card.id || card;
        const details = getCardDetails(cardId);
        const cardDiv = document.createElement("div");
        cardDiv.className = `card-item ${details.type}`;
        cardDiv.innerHTML = `
            <img src="images/card_${cardId}.jpeg" alt="${details.name}" class="card-image" onerror="this.style.opacity='0.2';">
        `;
        handDOM.appendChild(cardDiv);
    });

    // 2. Bench
    benchDOM.innerHTML = "";
    const bench = playerData.bench || [];
    bench.forEach(pokemon => {
        if (!pokemon) return;
        const cardId = pokemon.id || pokemon;
        const details = getCardDetails(cardId);
        const cardDiv = document.createElement("div");
        cardDiv.className = `card-item pokemon`;
        cardDiv.innerHTML = `
            <img src="images/card_${cardId}.jpeg" alt="${details.name}" class="card-image" onerror="this.style.opacity='0.2';">
        `;
        benchDOM.appendChild(cardDiv);
    });

    // 3. Active Pokémon
    activeDOM.innerHTML = "";
    const activeList = playerData.active || [];
    if (activeList.length > 0 && activeList[0]) {
        const active = activeList[0];
        const cardId = active.id || active;
        const details = getCardDetails(cardId);
        const hpPercent = Math.max(0, Math.min(100, ((active.hp || 100) / (active.maxHp || 100)) * 100));
        activeDOM.innerHTML = `
            <div class="active-pokemon-card ${pClass}">
                <img src="images/card_${cardId}.jpeg" alt="${details.name}" class="active-card-image" onerror="this.style.opacity='0.2';">
                <div class="active-overlay">
                    <div style="font-size: 0.8rem; font-weight: bold; color: var(--text-primary);">HP: ${active.hp || 100}/${active.maxHp || 100}</div>
                    <div class="active-hp-bar">
                        <div class="active-hp-inner" style="width: ${hpPercent}%"></div>
                    </div>
                </div>
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
                logsList.push(`Player ${p.player + 1} chose option indices: [${p.action.join(", ")}]`);
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

// Load Chart.js library (already included via CDN in HTML)

// Tab navigation handling
const tabPlaybackBtn = document.getElementById('tab-playback');
const tabAnalyticsBtn = document.getElementById('tab-analytics');
const playbackSection = document.getElementById('playback-section');
const analyticsSection = document.getElementById('analytics-section');

function showPlayback() {
  playbackSection.style.display = 'block';
  analyticsSection.style.display = 'none';
  tabPlaybackBtn.classList.add('active');
  tabAnalyticsBtn.classList.remove('active');
}
function showAnalytics() {
  playbackSection.style.display = 'none';
  analyticsSection.style.display = 'block';
  tabAnalyticsBtn.classList.add('active');
  tabPlaybackBtn.classList.remove('active');
  loadAnalytics();
}

tabPlaybackBtn.addEventListener('click', showPlayback);
tabAnalyticsBtn.addEventListener('click', showAnalytics);

// Load analytics data and render chart
let analyticsChart = null;
function loadAnalytics() {
  // Prevent reloading if already rendered
  if (analyticsChart) return;
  Promise.all([
    fetch('/versions/version_history.json').then(r => r.ok ? r.json() : []),
    fetch('/logs/kaggle_summary/kaggle_results_summary.json').then(r => r.ok ? r.json() : [])
  ]).then(([versions, kaggle]) => {
    const ctx = document.getElementById('analytics-chart').getContext('2d');
    // Example: line chart of version scores over time
    const versionLabels = versions.map(v => v.version_id || v.version);
    const versionScores = versions.map(v => v.version_score || 0);
    const kaggleWins = kaggle.filter(e => e.result === 'win').length;
    const kaggleLosses = kaggle.filter(e => e.result === 'loss').length;
    const kaggleDraws = kaggle.filter(e => e.result === 'draw').length;
    const data = {
      labels: versionLabels,
      datasets: [{
        label: 'Version Score',
        data: versionScores,
        borderColor: 'var(--accent-blue)',
        backgroundColor: 'rgba(59,130,246,0.2)',
        tension: 0.4,
        yAxisID: 'y'
      }, {
        type: 'bar',
        label: 'Kaggle Wins',
        data: versionLabels.map(() => kaggleWins),
        backgroundColor: 'var(--accent-green)'
      }, {
        type: 'bar',
        label: 'Kaggle Losses',
        data: versionLabels.map(() => kaggleLosses),
        backgroundColor: 'var(--accent-red)'
      }]
    };
    const config = {
      type: 'line',
      data: data,
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Analytics Dashboard' }
        },
        scales: {
          y: { beginAtZero: true, title: { display: true, text: 'Score' } },
          y1: { beginAtZero: true, display: false }
        }
      }
    };
    analyticsChart = new Chart(ctx, config);
  }).catch(err => console.error('Failed to load analytics data:', err));
}

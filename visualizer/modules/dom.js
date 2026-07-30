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

const p1Hand = document.getElementById("player-hand");
const p1Bench = document.getElementById("player-bench");
const p1Active = document.getElementById("player-active");
const p1Prizes = document.getElementById("player-prizes");
const p1Deck = document.getElementById("player-deck");

const p2Hand = document.getElementById("opp-hand");
const p2Bench = document.getElementById("opp-bench");
const p2Active = document.getElementById("opp-active");
const p2Prizes = document.getElementById("opp-prizes");
const p2Deck = document.getElementById("opp-deck");

const fileSelect = document.getElementById("game-file-select");

const tabPlaybackBtn = document.getElementById('tab-playback');
const tabAnalyticsBtn = document.getElementById('tab-analytics');
const playbackSection = document.getElementById('playback-section');
const analyticsSection = document.getElementById('analytics-section');

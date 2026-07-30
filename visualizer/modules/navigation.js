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

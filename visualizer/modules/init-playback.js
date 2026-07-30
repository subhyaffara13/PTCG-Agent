function initPlayback() {
    if (gameSteps.length === 0) return;

    totalStepsTxt.textContent = gameSteps.length - 1;
    timelineSlider.max = gameSteps.length - 1;
    timelineSlider.value = 0;

    btnNext.disabled = gameSteps.length <= 1;
    btnPrev.disabled = true;

    renderStep(0);
}

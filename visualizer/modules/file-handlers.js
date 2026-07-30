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

loadAvailableLogs();

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

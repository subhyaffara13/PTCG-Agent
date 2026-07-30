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

let analyticsChart = null;

function loadAnalytics() {
  if (analyticsChart) return;
  Promise.all([
    fetch('/versions/version_history.json').then(r => r.ok ? r.json() : []),
    fetch('/logs/kaggle_summary/kaggle_results_summary.json').then(r => r.ok ? r.json() : [])
  ]).then(([versions, kaggle]) => {
    const ctx = document.getElementById('analytics-chart').getContext('2d');
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

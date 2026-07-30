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

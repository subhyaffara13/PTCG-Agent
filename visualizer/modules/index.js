// Module index - loads all modules in dependency order
const MODULES = [
  'modules/card-database.js',
  'modules/state.js',
  'modules/dom.js',
  'modules/log-loader.js',
  'modules/file-handlers.js',
  'modules/init-playback.js',
  'modules/navigation.js',
  'modules/player-board.js',
  'modules/renderer.js',
  'modules/tabs.js',
  'modules/analytics.js'
];

(function loadModules(idx) {
  if (idx >= MODULES.length) return;
  const script = document.createElement('script');
  script.src = MODULES[idx];
  script.onload = () => loadModules(idx + 1);
  script.onerror = () => loadModules(idx + 1);
  document.head.appendChild(script);
})(0);

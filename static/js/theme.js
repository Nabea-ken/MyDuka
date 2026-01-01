const toggle = document.getElementById('themeToggle');
const root = document.documentElement;

toggle.addEventListener('click', () => {
  const theme = root.getAttribute('data-theme');
  root.setAttribute('data-theme', theme === 'dark' ? 'light' : 'dark');
});

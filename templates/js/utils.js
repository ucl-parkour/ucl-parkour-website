function setColorScheme(darkMode) {
  const root = document.querySelector(":root");
  if (darkMode) {
    root.classList.add("dark");
  } else {
    root.classList.remove("dark");
  }
}

if (window.matchMedia) {
  const colorSchemeMatch = window.matchMedia("(prefers-color-scheme: dark)");
  const prefersDark = colorSchemeMatch.matches;
  setColorScheme(prefersDark);

  // Detect changes in the user's system theme and update color scheme accordingly.
  colorSchemeMatch.addEventListener("change", (event) => {
    const prefersDark = event.matches;
    setColorScheme(prefersDark);
  });
}

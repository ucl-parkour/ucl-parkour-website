// Color scheme
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

// Mobile dropdown menu
for (const menu of document.querySelectorAll(".js-dropdown")) {
  registerDropdownMenu(menu);
}

function registerDropdownMenu(menu) {
  const button = menu.querySelector(".js-dropdown__button");
  const items = menu.querySelectorAll(".js-dropdown__item");
  button.addEventListener("click", toggle);

  function toggle() {
    menu.classList.toggle("site-header__item-group--mobile-open");
    for (const item of items) {
      item.toggleAttribute("hidden");
    }
  }
}

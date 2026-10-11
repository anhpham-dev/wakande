"use strict";

(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector(".theme-toggle");
  const menuButton = document.querySelector(".menu-toggle");
  const sidebar = document.querySelector(".sidebar");
  const searchForm = document.querySelector(".search");
  const searchInput = document.querySelector("#docs-search");
  const searchStatus = document.querySelector("#search-status");
  const sections = [...document.querySelectorAll(".doc-section")];
  const links = [...document.querySelectorAll(".nav-link")];
  const searchable = sections.map(section => ({
    section,
    text: section.textContent.toLowerCase(),
  }));

  const preference = window.matchMedia("(prefers-color-scheme: dark)");
  let savedTheme = null;
  try { savedTheme = localStorage.getItem("wakande-docs-theme"); } catch { /* Storage may be disabled. */ }
  let explicitTheme = savedTheme === "light" || savedTheme === "dark";

  function applyTheme(theme) {
    root.dataset.theme = theme;
    themeButton.setAttribute("aria-pressed", String(theme === "dark"));
    themeButton.setAttribute("aria-label", `Switch to ${theme === "dark" ? "light" : "dark"} theme`);
  }
  applyTheme(explicitTheme ? savedTheme : preference.matches ? "dark" : "light");
  themeButton.hidden = false;
  themeButton.addEventListener("click", () => {
    const theme = root.dataset.theme === "dark" ? "light" : "dark";
    explicitTheme = true;
    applyTheme(theme);
    try { localStorage.setItem("wakande-docs-theme", theme); } catch { /* Keep the current session's choice. */ }
  });
  preference.addEventListener("change", event => {
    if (!explicitTheme) applyTheme(event.matches ? "dark" : "light");
  });

  sidebar.classList.add("enhanced");
  menuButton.hidden = false;
  function setMenu(open) {
    sidebar.classList.toggle("is-open", open);
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.textContent = open ? "Close" : "Menu";
  }
  menuButton.addEventListener("click", () => setMenu(menuButton.getAttribute("aria-expanded") !== "true"));

  function setActive(id) {
    for (const link of links) {
      const active = link.hash === `#${id}`;
      link.classList.toggle("active", active);
      if (active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    }
  }

  function filterSections() {
    const query = searchInput.value.trim();
    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const { section, text } of searchable) {
      const matches = terms.every(term => text.includes(term));
      section.hidden = !matches;
      if (matches) count++;
    }
    searchStatus.hidden = !query;
    searchStatus.textContent = count
      ? `${count} ${count === 1 ? "section matches" : "sections match"} “${query}”. Clear the search to see all topics.`
      : `No sections match “${query}”. Try “variables”, “Python”, or “arithmetic”.`;
    updateActiveSection();
  }
  searchForm.hidden = false;
  searchForm.addEventListener("submit", event => event.preventDefault());
  searchInput.addEventListener("input", filterSections);

  function visitAnchor() {
    const id = window.location.hash.slice(1) || "overview";
    const target = document.getElementById(id);
    if (!target || !target.classList.contains("doc-section")) return;
    if (searchInput.value) {
      searchInput.value = "";
      filterSections();
      target.scrollIntoView();
    }
    setActive(id);
  }
  for (const link of document.querySelectorAll('a[href^="#"]')) {
    link.addEventListener("click", () => {
      const target = document.getElementById(link.hash.slice(1));
      if (target?.classList.contains("doc-section")) {
        searchInput.value = "";
        filterSections();
        setActive(target.id);
      }
      if (window.matchMedia("(max-width: 760px)").matches && sidebar.classList.contains("is-open")) {
        setMenu(false);
        // Keep keyboard focus on the destination when the navigation is hidden.
        if (target) {
          target.setAttribute("tabindex", "-1");
          target.focus({ preventScroll: true });
        }
      }
    });
  }
  window.addEventListener("hashchange", visitAnchor);
  visitAnchor();

  document.addEventListener("keydown", event => {
    const editing = event.target instanceof Element && event.target.closest("input, textarea, select, [contenteditable]");
    if (event.key === "/" && !editing && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      if (window.matchMedia("(max-width: 760px)").matches) setMenu(true);
      searchInput.focus();
    }
    if (event.key === "Escape") {
      if (searchInput.value) {
        searchInput.value = "";
        filterSections();
      } else if (sidebar.classList.contains("is-open")) {
        setMenu(false);
        menuButton.focus();
      }
    }
  });

  function updateActiveSection() {
    const visible = sections.filter(section => !section.hidden);
    if (!visible.length) {
      setActive("");
      return;
    }
    const threshold = window.matchMedia("(max-width: 760px)").matches ? 140 : 160;
    let current = visible[0];
    for (const section of visible) {
      if (section.getBoundingClientRect().top <= threshold) current = section;
    }
    setActive(current.id);
  }
  let scrollPending = false;
  window.addEventListener("scroll", () => {
    if (scrollPending) return;
    scrollPending = true;
    window.requestAnimationFrame(() => {
      updateActiveSection();
      scrollPending = false;
    });
  }, { passive: true });

  for (const block of document.querySelectorAll(".code-block, .hero-code")) {
    const code = block.querySelector("pre code");
    const header = block.querySelector(".code-header");
    if (!code || !header) continue;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy-button";
    button.textContent = "Copy";
    button.setAttribute("aria-label", `Copy ${header.textContent.trim()} code`);
    header.append(button);
    button.addEventListener("click", async () => {
      try {
        if (!navigator.clipboard?.writeText) throw new Error("Clipboard unavailable");
        await navigator.clipboard.writeText(code.textContent);
        button.textContent = "Copied!";
      } catch {
        const selection = window.getSelection();
        if (selection) {
          const range = document.createRange();
          range.selectNodeContents(code);
          selection.removeAllRanges();
          selection.addRange(range);
        }
        button.textContent = "Selected";
        searchStatus.hidden = false;
        searchStatus.textContent = "Code selected. Press Ctrl+C or Command+C to copy, or use your device's copy menu.";
      }
      window.setTimeout(() => { button.textContent = "Copy"; }, 2000);
    });
  }
})();

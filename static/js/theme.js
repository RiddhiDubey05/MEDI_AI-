document.addEventListener("DOMContentLoaded", function () {
  const themeBtn = document.getElementById("themeBtn");
  const html = document.documentElement;

  // Load preference
  const savedTheme = localStorage.getItem("mediai_theme") || "light";
  html.setAttribute("data-theme", savedTheme);
  themeBtn.textContent = savedTheme === "dark" ? "☀️" : "🌙";

  themeBtn.addEventListener("click", function () {
    const currentTheme = html.getAttribute("data-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";
    
    html.setAttribute("data-theme", newTheme);
    localStorage.setItem("mediai_theme", newTheme);
    
    themeBtn.textContent = newTheme === "dark" ? "☀️" : "🌙";
  });
});

const toggleBtn = document.getElementById("theme-toggle");
const body = document.body;

// Load saved theme
if (localStorage.getItem("theme") === "light") {
  body.classList.add("light");
  toggleBtn.textContent = "🌙";
}

toggleBtn.addEventListener("click", () => {
  body.classList.toggle("light");

  if (body.classList.contains("light")) {
    toggleBtn.textContent = "🌙";
    localStorage.setItem("theme", "light");
  } else {
    toggleBtn.textContent = "☀️";
    localStorage.setItem("theme", "dark");
  }
});

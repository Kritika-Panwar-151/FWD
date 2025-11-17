// Initialize icons
document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons();
});

// Dropdown logic
document.addEventListener("DOMContentLoaded", () => {
  const profileBtn = document.getElementById("profileBtn");
  const profileMenu = document.getElementById("profileMenu");

  if (!profileBtn || !profileMenu) return;

  profileBtn.addEventListener("click", e => {
    e.stopPropagation();
    profileMenu.classList.toggle("is-open");
  });

  document.addEventListener("click", e => {
    if (!profileMenu.contains(e.target) && !profileBtn.contains(e.target)) {
      profileMenu.classList.remove("is-open");
    }
  });

  document.addEventListener("keydown", e => {
    if (e.key === "Escape") profileMenu.classList.remove("is-open");
  });
});

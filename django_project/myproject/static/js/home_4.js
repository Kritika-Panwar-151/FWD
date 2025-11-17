// Initialize icons
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    lucide.createIcons();
  }
});

// Smooth scroll helper
function scrollToId(id) {
  const el = document.getElementById(id) || document.querySelector(`[name="${id}"]`);
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

// Attach scroll to buttons
document.addEventListener("DOMContentLoaded", () => {
  const searchBtn1 = document.getElementById("searchHostelBtn");
  const searchBtn2 = document.getElementById("searchHostelBtn2");
  const headerSearchBtn = document.getElementById("headerSearchBtn");

  if (searchBtn1) {
    searchBtn1.addEventListener("click", () => scrollToId("chooseHostel"));
  }
  if (searchBtn2) {
    searchBtn2.addEventListener("click", () => scrollToId("chooseHostel"));
  }
  if (headerSearchBtn) {
    headerSearchBtn.addEventListener("click", () => scrollToId("chooseHostel"));
  }
});

// Profile dropdown toggle
document.addEventListener("DOMContentLoaded", () => {
  const profileBtn = document.getElementById("profileBtn");
  const profileMenu = document.getElementById("profileMenu");

  if (!profileBtn || !profileMenu) return;

  // Open/close on icon click
  profileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    profileMenu.classList.toggle("is-open");
  });

  // Close when clicking outside
  document.addEventListener("click", (e) => {
    if (
      profileMenu.classList.contains("is-open") &&
      !profileMenu.contains(e.target) &&
      !profileBtn.contains(e.target)
    ) {
      profileMenu.classList.remove("is-open");
    }
  });

  // Close with ESC key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      profileMenu.classList.remove("is-open");
    }
  });
});

// Initialize icons
document.addEventListener("DOMContentLoaded", () => {
    if (window.lucide) lucide.createIcons();
});

// Smooth scroll
function scrollToId(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth" });
}

// Buttons
document.getElementById("searchHostelBtn").onclick = () => scrollToId("chooseHostel");
document.getElementById("headerSearchBtn").onclick = () => scrollToId("chooseHostel");

// Profile popup toggle
const profileIcon = document.querySelector(".profile-box");
const profileMenu = document.getElementById("profileMenu");

profileIcon.addEventListener("click", () => {
    profileMenu.classList.toggle("open");
});

// Close popup when clicking outside
document.addEventListener("click", (e) => {
    if (!profileIcon.contains(e.target) && !profileMenu.contains(e.target)) {
        profileMenu.classList.remove("open");
    }
});

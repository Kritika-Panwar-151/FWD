/* ============================================
   INITIALIZE ICONS
============================================ */
document.addEventListener("DOMContentLoaded", () => {
    if (window.lucide) {
        lucide.createIcons();
    }
});


/* ============================================
   PROFILE DROPDOWN LOGIC
============================================ */
const profileBtn = document.getElementById("profileBtn");
const profileMenu = document.getElementById("profileMenu");

if (profileBtn && profileMenu) {
    // Open / close
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
        if (e.key === "Escape") profileMenu.classList.remove("is-open");
    });
}


/* ============================================
   SEARCH SCROLL (if needed)
============================================ */
function scrollToId(id) {
    const el = document.getElementById(id);
    if (el) {
        el.scrollIntoView({ behavior: "smooth" });
    }
}


/* ============================================
   DJANGO LOGOUT
============================================ */
function logoutUser() {
    window.location.href = "/logout/";
}
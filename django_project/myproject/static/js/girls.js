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
    // Toggle dropdown
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

    // Close with Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") profileMenu.classList.remove("is-open");
    });
}


/* ============================================
   SEARCH SCROLL (if used)
============================================ */
function scrollToId(id) {
    const el = document.getElementById(id) || document.querySelector(`[name="${id}"]`);
    if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
}


/* ============================================
   DJANGO LOGOUT
============================================ */
function logoutUser() {
    window.location.href = "/logout/";
}

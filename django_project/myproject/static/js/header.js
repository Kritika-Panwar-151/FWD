document.addEventListener("DOMContentLoaded", () => {
    
    /* ICONS */
    if (window.lucide) {
        lucide.createIcons();
    }

    /* PROFILE DROPDOWN */
    const profileBtn = document.getElementById("profileBtn");
    const profileMenu = document.getElementById("profileMenu");

    if (profileBtn && profileMenu) {

        profileBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            profileMenu.classList.toggle("is-open");
        });

        document.addEventListener("click", (e) => {
            if (!profileMenu.contains(e.target) && !profileBtn.contains(e.target)) {
                profileMenu.classList.remove("is-open");
            }
        });

        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") profileMenu.classList.remove("is-open");
        });
    }

    /* SEARCH BUTTON */
    const search = document.getElementById("headerSearchBtn");

    if (search) {
        search.addEventListener("click", () => {
            if (document.querySelector("#chooseHostel")) {
                document.querySelector("#chooseHostel")
                    .scrollIntoView({ behavior: "smooth" });
            } else {
                window.location.href = "/home/#chooseHostel";
            }
        });
    }
});

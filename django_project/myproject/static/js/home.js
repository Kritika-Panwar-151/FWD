// === Smooth navbar background on scroll (as per your original CSS) ===
window.addEventListener("scroll", () => {
    const navbar = document.querySelector(".navbar");
    if (window.scrollY > 50) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }
});

// === Smooth scroll for internal links ===
document.querySelectorAll(".navbar a").forEach(link => {
    link.addEventListener("click", e => {
        const href = link.getAttribute("href");
        
        // Only prevent default for internal anchor links (starting with #)
        if (href.startsWith("#")) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                // Scroll position adjusted for the fixed navbar height (~60px)
                window.scrollTo({
                    top: target.offsetTop - 60, 
                    behavior: "smooth"
                });
            }
        }
    });
});
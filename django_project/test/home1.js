// === Smooth navbar background on scroll ===
window.addEventListener("scroll", () => {
  const navbar = document.querySelector(".navbar");
  if (window.scrollY > 50) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
});

// === Fix for hero section disappearing / background gap issue ===
window.addEventListener("load", () => {
  const hero = document.querySelector(".hero");
  hero.style.backgroundAttachment = "fixed";
  hero.style.backgroundRepeat = "no-repeat";
  hero.style.backgroundSize = "cover";
});

// === Optional: Scroll to section on nav click ===
document.querySelectorAll(".navbar a").forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    const target = document.querySelector(link.getAttribute("href"));
    if (target) {
      window.scrollTo({
        top: target.offsetTop - 60,
        behavior: "smooth"
      });
    }
  });
});

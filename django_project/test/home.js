window.addEventListener("scroll", () => {
  const navbar = document.querySelector(".navbar");
  const hero = document.querySelector(".hero");

  // Add solid navbar when scrolled down
  if (window.scrollY > 80) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }

  // Smooth hero transition effect
  const scrollY = window.scrollY;
  const maxScroll = hero.offsetHeight / 2;
  const opacity = Math.min(scrollY / maxScroll, 1);
  hero.style.backgroundPositionY = `${scrollY * 0.4}px`;
  hero.style.opacity = 1 - opacity * 0.1;
});

document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) lucide.createIcons();
});

function openMap() {
  window.open("https://www.google.com/maps/search/BMSCE", "_blank");
}

document.querySelectorAll(".gallery-item").forEach(item => {
  let timer;

  item.addEventListener("mouseenter", () => {
    timer = setTimeout(() => {
      item.classList.add("zoomed");
    }, 500); // 2 seconds
  });

  item.addEventListener("mouseleave", () => {
    clearTimeout(timer);
    item.classList.remove("zoomed");
  });
});

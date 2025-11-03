const authBox = document.getElementById("authBox");
const goSignup = document.getElementById("goSignup");
const goLogin = document.getElementById("goLogin");

// Click toggles
goSignup.addEventListener("click", () => {
  authBox.classList.add("signup-mode");
});

goLogin.addEventListener("click", () => {
  authBox.classList.remove("signup-mode");
});

// Scroll toggles
window.addEventListener("wheel", (event) => {
  if (event.deltaY > 0) {
    authBox.classList.add("signup-mode");
  } else if (event.deltaY < 0) {
    authBox.classList.remove("signup-mode");
  }
});

// Swipe / Drag toggle (mouse or touch)
let startY = 0;
let endY = 0;

// For mouse
window.addEventListener("mousedown", (e) => {
  startY = e.clientY;
});
window.addEventListener("mouseup", (e) => {
  endY = e.clientY;
  handleSwipe();
});

// For touch devices
window.addEventListener("touchstart", (e) => {
  startY = e.touches[0].clientY;
});
window.addEventListener("touchend", (e) => {
  endY = e.changedTouches[0].clientY;
  handleSwipe();
});

function handleSwipe() {
  if (startY - endY > 80) {
    // Swipe up → show signup
    authBox.classList.add("signup-mode");
  } else if (endY - startY > 80) {
    // Swipe down → show login
    authBox.classList.remove("signup-mode");
  }
}

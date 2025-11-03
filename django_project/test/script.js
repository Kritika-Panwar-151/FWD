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

// Mouse scroll to switch forms
window.addEventListener("wheel", (event) => {
  if (event.deltaY > 0) {
    // Scroll down → show Sign Up
    authBox.classList.add("signup-mode");
  } else if (event.deltaY < 0) {
    // Scroll up → show Login
    authBox.classList.remove("signup-mode");
  }
});
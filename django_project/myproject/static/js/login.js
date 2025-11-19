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

// Scroll toggles (mouse + touchpad)
let scrollTimeout;
window.addEventListener("wheel", (event) => {
  clearTimeout(scrollTimeout);
  scrollTimeout = setTimeout(() => {
    if (event.deltaY > 30) {
      authBox.classList.add("signup-mode");
    } else if (event.deltaY < -30) {
      authBox.classList.remove("signup-mode");
    }
  }, 50);
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

//Password Strength Validation
const signupPassword = document.getElementById("signupPassword");
const passwordFeedback = document.getElementById("passwordFeedback");
const signupBtn = document.getElementById("signupBtn");

signupPassword.addEventListener("input", () => {
  const password = signupPassword.value;
  const isStrong = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/.test(password);

  if (isStrong) {
    passwordFeedback.textContent = "✅ Strong password!";
    passwordFeedback.classList.add("valid");
    signupBtn.disabled = false;
  } else {
    passwordFeedback.textContent = "❌ Weak password: must contain 8 characters 1 uppercase,1 lowercase,1 number, and 1 special character.";
    passwordFeedback.classList.remove("valid");
    signupBtn.disabled = true;
  }

  passwordFeedback.style.display = "block";
});

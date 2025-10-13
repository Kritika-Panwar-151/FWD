const formTitle = document.getElementById("formTitle");
const formSubtext = document.getElementById("formSubtext");
const submitBtn = document.getElementById("submitBtn");
const switchBtn = document.getElementById("switchBtn");
const switchPrompt = document.getElementById("switchPrompt");
const loginOptions = document.getElementById("loginOptions");

let isSignUp = false;

switchBtn.addEventListener("click", () => {
  isSignUp = !isSignUp;
  if (isSignUp) {
    formTitle.textContent = "Create Account";
    formSubtext.textContent = "Join our community of travelers today";
    submitBtn.textContent = "Create Account";
    switchPrompt.textContent = "Already have an account?";
    switchBtn.textContent = "Sign In";
    loginOptions.style.display = "none";
  } else {
    formTitle.textContent = "Welcome Back";
    formSubtext.textContent = "Sign in to continue your journey";
    submitBtn.textContent = "Sign In";
    switchPrompt.textContent = "Don't have an account?";
    switchBtn.textContent = "Sign Up";
    loginOptions.style.display = "flex";
  }
});

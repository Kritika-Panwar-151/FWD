document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("bookingForm");
  if (!form) return; // Exit if user already has a booking

  // --- Selectors ---
  const usnInput = document.getElementById("usn");
  const phoneInput = document.getElementById("phone");
  const usnError = document.getElementById("usnError");
  const phoneError = document.getElementById("phoneError");
  
  const prefs = [
    form.querySelector('select[name="pref_1"]'),
    form.querySelector('select[name="pref_2"]'),
    form.querySelector('select[name="pref_3"]')
  ];

  // --- Timing variables for DB check ---
  let typingTimer;
  const doneTypingInterval = 400; // 0.4 seconds pause before checking DB

  // ==========================================
  // 1. REAL-TIME USN & DATABASE VALIDATION
  // ==========================================
  usnInput.addEventListener("input", () => {
    const val = usnInput.value.trim();
    usnError.textContent = ""; // Clear errors immediately as they type

    if (val.length > 10) {
      usnError.textContent = "USN cannot exceed 10 characters";
    } else {
      // Background check for "Already Registered"
      clearTimeout(typingTimer);
      typingTimer = setTimeout(async () => {
        if (val.length >= 5) {
          try {
            const response = await fetch(`/check-usn/?usn=${val}`);
            const data = await response.json();
            if (data.is_taken) {
              usnError.textContent = "This USN is already registered";
            }
          } catch (err) {
            console.error("Database check failed", err);
          }
        }
      }, doneTypingInterval);
    }
  });

  // ==========================================
  // 2. REAL-TIME PHONE VALIDATION
  // ==========================================
  phoneInput.addEventListener("input", () => {
    const val = phoneInput.value.trim();
    const isNotDigit = /\D/.test(val); // Matches any character that is NOT a digit

    if (isNotDigit) {
      phoneError.textContent = "Only digits (0-9) are allowed";
    } else if (val.length > 10) {
      phoneError.textContent = "Phone number cannot exceed 10 digits";
    } else {
      phoneError.textContent = ""; // Clear message if back to valid
    }
  });

  // ==========================================
  // 3. PREVENT DUPLICATE PREFERENCES
  // ==========================================
  function updatePrefs() {
    const selected = prefs.map(p => p.value).filter(Boolean);

    prefs.forEach(select => {
      Array.from(select.options).forEach(opt => {
        opt.disabled =
          opt.value &&
          selected.includes(opt.value) &&
          opt.value !== select.value;
      });
    });
  }

  prefs.forEach(p => p.addEventListener("change", updatePrefs));

  // ==========================================
  // 4. FINAL SUBMISSION (AJAX)
  // ==========================================
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Reset errors and re-check length
    let isValid = true;
    if (usnInput.value.trim().length !== 10) {
      usnError.textContent = "USN must be exactly 10 characters";
      isValid = false;
    }
    if (!/^\d{10}$/.test(phoneInput.value.trim())) {
      phoneError.textContent = "Phone must be exactly 10 digits";
      isValid = false;
    }

    // Stop if there is any visible error text (including DB check results)
    if (!isValid || usnError.textContent !== "" || phoneError.textContent !== "") {
      return;
    }

    const data = new FormData(form);
    const res = await fetch("", {
      method: "POST",
      body: data,
      headers: { "X-Requested-With": "XMLHttpRequest" }
    });

    if (res.ok) {
      location.reload(); // Success!
    } else {
      usnError.textContent = "Submission failed. USN/Email might be taken.";
    }
  });
});
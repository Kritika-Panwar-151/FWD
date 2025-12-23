document.addEventListener("DOMContentLoaded", () => {

  // Init icons
  if (typeof lucide !== "undefined") {
    lucide.createIcons();
  }

  const form = document.getElementById("bookingForm");
  const successSection = document.getElementById("bookingSuccess");

  if (!form || !successSection) {
    console.error("❌ Booking form or success section missing");
    return;
  }

  // ===============================
  // PREVENT DUPLICATE PREFERENCES
  // ===============================
  const prefSelects = [
    form.querySelector('select[name="pref_1"]'),
    form.querySelector('select[name="pref_2"]'),
    form.querySelector('select[name="pref_3"]')
  ];

  function updatePreferenceOptions() {
    // Get all selected values
    const selectedValues = prefSelects
      .map(select => select.value)
      .filter(value => value !== "");

    prefSelects.forEach(select => {
      Array.from(select.options).forEach(option => {
        if (
          option.value !== "" &&
          selectedValues.includes(option.value) &&
          option.value !== select.value
        ) {
          option.disabled = true;
        } else {
          option.disabled = false;
        }
      });
    });
  }

  // Attach change listener
  prefSelects.forEach(select => {
    select.addEventListener("change", updatePreferenceOptions);
  });

  // ===============================
  // FORM SUBMIT (SUCCESS SCREEN)
  // ===============================
  form.addEventListener("submit", function (e) {
    e.preventDefault(); // STOP PAGE RELOAD

    const data = new FormData(form);

    // Final safety check (just in case)
    const prefs = [
      data.get("pref_1"),
      data.get("pref_2"),
      data.get("pref_3")
    ];

    const uniquePrefs = new Set(prefs);
    if (uniquePrefs.size !== prefs.length) {
      alert("Please select different hostels for each preference.");
      return;
    }

    // Fill success summary
    document.getElementById("s-name").textContent = data.get("name") || "-";
    document.getElementById("s-email").textContent = data.get("email") || "-";
    document.getElementById("s-phone").textContent = data.get("phone") || "-";
    document.getElementById("s-hostel").textContent = data.get("hostel_type") || "-";
    document.getElementById("s-year").textContent = data.get("year") || "-";
    document.getElementById("s-pref1").textContent = data.get("pref_1") || "-";
    document.getElementById("s-pref2").textContent = data.get("pref_2") || "-";
    document.getElementById("s-pref3").textContent = data.get("pref_3") || "-";

    // Hide form
    form.style.display = "none";

    // Show success
    successSection.style.display = "block";
    successSection.scrollIntoView({ behavior: "smooth" });
  });

});

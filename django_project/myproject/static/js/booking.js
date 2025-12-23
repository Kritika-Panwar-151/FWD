document.addEventListener("DOMContentLoaded", () => {

  if (typeof lucide !== "undefined") {
    lucide.createIcons();
  }

  const form = document.getElementById("bookingForm");

  // 🔒 If form does not exist → booking already done
  if (!form) return;

  // ---------- Prevent duplicate preferences ----------
  const prefs = [
    form.querySelector('select[name="pref_1"]'),
    form.querySelector('select[name="pref_2"]'),
    form.querySelector('select[name="pref_3"]')
  ];

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

  // ---------- Submit ----------
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = new FormData(form);

    const res = await fetch("", {
      method: "POST",
      body: data,
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      }
    });

    if (!res.ok) {
      const result = await res.json();
      alert("Booking failed: " + (result.message || "Unknown error"));
      return;
    }

    // 🔥 Backend is source of truth → reload
    location.reload();
  });

});

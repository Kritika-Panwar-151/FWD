document.addEventListener("DOMContentLoaded", () => {

  const gender = localStorage.getItem("unistayGender");

  const displayField = document.getElementById("hostelTypeDisplay");
  const hiddenField = document.getElementById("hostelType");

  if (gender === "boys") {  
    displayField.value = "Boys Hostel";
    hiddenField.value = "boys";
  } else if (gender === "girls") {
    displayField.value = "Girls Hostel";
    hiddenField.value = "girls";
  } else {
    displayField.value = "Not specified";
    hiddenField.value = "";
  }

  const form = document.getElementById("bookingForm");
  const successSection = document.getElementById("bookingSuccess");

  if (!form || !successSection) {
    console.error("❌ Booking form or success section missing");
    return;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault(); // STOP PAGE RELOAD

    const data = new FormData(form);

    // Fill summary safely
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

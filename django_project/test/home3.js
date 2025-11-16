/* init icons */
lucide.createIcons();

/* small UX niceties */
function scrollToId(id){
    const el = document.getElementById(id) || document.querySelector(`[name="${id}"]`);
    if(el){ el.scrollIntoView({behavior:'smooth', block:'start'}) }
}

lucide.createIcons();

// Smooth scroll logic for the "Search Hostels" button in the Hero and CTA sections
document.getElementById("searchHostelBtn").addEventListener("click", function () {
    // The target ID for this button is hardcoded to "chooseHostel" (the hostel selection section)
    document.getElementById("chooseHostel").scrollIntoView({
        behavior: "smooth"
    });
});

// Smooth scroll logic for the Search icon in the header
document.getElementById("headerSearchBtn").addEventListener("click", function () {
    // The target ID for this button is hardcoded to "chooseHostel" (the hostel selection section)
    document.getElementById("chooseHostel").scrollIntoView({
        behavior: "smooth"
    });
});
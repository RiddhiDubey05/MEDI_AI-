document.addEventListener("DOMContentLoaded", function(){
  const modal    = document.getElementById("sosModal");
  const locBox   = document.getElementById("locBox");
  const shareBtn = document.getElementById("shareLocBtn");

  document.getElementById("sosBtn").addEventListener("click", function(){
    locBox.textContent = "Tap 'Share Location' to get your live GPS coordinates.";
    shareBtn.textContent = "📍 Share Location";
    shareBtn.disabled = false;
    modal.classList.add("open");
  });

  document.getElementById("closeSosBtn").addEventListener("click", function(){
    modal.classList.remove("open");
  });

  modal.addEventListener("click", function(e){
    if(e.target === modal) modal.classList.remove("open");
  });

  shareBtn.addEventListener("click", function(){
    shareBtn.textContent = "Locating…";
    shareBtn.disabled = true;
    if(!navigator.geolocation){
      locBox.textContent = "Geolocation is not supported by this browser.";
      shareBtn.textContent = "Unavailable";
      return;
    }
    navigator.geolocation.getCurrentPosition(
      function(pos){
        const lat = pos.coords.latitude.toFixed(6);
        const lng = pos.coords.longitude.toFixed(6);
        const url = `https://maps.google.com/?q=${lat},${lng}`;
        locBox.innerHTML = `<div>
          <strong style="color:var(--accent);display:block;margin-bottom:6px">📍 Location Found</strong>
          <strong>${lat}, ${lng}</strong><br><br>
          <a href="${url}" target="_blank" style="color:var(--accent);font-weight:700;font-size:13px">Open in Google Maps →</a>
          <br><br><span style="font-size:11px;color:var(--ink-muted)">Share this link with emergency services</span>
        </div>`;
        shareBtn.textContent = "🔄 Refresh";
        shareBtn.disabled = false;
      },
      function(err){
        locBox.textContent = "Could not get location: " + err.message + ". Please allow location access.";
        shareBtn.textContent = "Retry";
        shareBtn.disabled = false;
      },
      { enableHighAccuracy: true, timeout: 12000 }
    );
  });
});
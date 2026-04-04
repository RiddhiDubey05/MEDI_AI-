let activeId = null;
const LS_KEY = "mediai_patients";

async function loadSidebar(){
  const res = await fetch("/api/patients");
  let patients = await res.json();
  
  // Sync with localStorage
  const local = JSON.parse(localStorage.getItem(LS_KEY) || "[]");
  if(local.length > patients.length) {
    patients = local;
  }
  localStorage.setItem(LS_KEY, JSON.stringify(patients));

  const list = document.getElementById("ptList");
  if(!patients.length){
    list.innerHTML = `<div class="empty-sb">No records yet.<br>Run a diagnosis to save a record.</div>`;
    return;
  }

  list.innerHTML = patients.map(p => {
    const visitDate = new Date(p.date).toLocaleDateString("en-IN",{day:"numeric",month:"short",year:"2-digit"});
    const meta = [
      p.age ? p.age+" yrs" : "", 
      p.sex || "",
      `Visit: ${visitDate}`
    ].filter(Boolean).join(" · ");
    return `<div class="pt-item ${p.id===activeId?"active":""}" data-id="${p.id}">
      <div class="pt-info">
        <div class="pt-name">${p.name||"Unnamed Patient"}</div>
        <div class="pt-meta">${meta}</div>
      </div>
      <button class="pt-del" data-del="${p.id}" title="Delete record">❌</button>
    </div>`;
  }).join("");

  list.querySelectorAll(".pt-item").forEach(el => {
    el.addEventListener("click", function(e){
      if(e.target.classList.contains("pt-del")) return;
      loadPatient(this.dataset.id, patients);
    });
  });

  list.querySelectorAll(".pt-del").forEach(btn => {
    btn.addEventListener("click", function(e){
      e.stopPropagation();
      if(confirm("Are you sure you want to delete this patient record?")) {
        deletePatient(this.dataset.del);
      }
    });
  });
}

function loadPatient(id, patients){
  const p = patients.find(x => x.id === id);
  if(!p) return;
  activeId = id;
  document.getElementById("patientName").value   = p.name||"";
  document.getElementById("age").value            = p.age||"";
  document.getElementById("sex").value            = p.sex||"";
  document.getElementById("phone").value          = p.phone||"";
  document.getElementById("symptoms").value       = p.symptoms||"";
  document.getElementById("durationVal").value    = p.durationVal||"";
  document.getElementById("durationUnit").value   = p.durationUnit||"days";
  document.getElementById("medicalHistory").value = p.medicalHistory||"";
  document.getElementById("medications").value    = p.medications||"";
  document.getElementById("allergies").value      = p.allergies||"";
  document.getElementById("nextVisit").value      = p.nextVisit||"";
  
  if(window.renderResults && p.results) renderResults(p.results);
  else if(p.results) {
      // Fallback for app.js displayResults if renderResults doesn't exist
      if(typeof displayResults === 'function') displayResults(p.results.diagnoses || p.results);
  }
  else showEmpty();

  document.querySelectorAll(".pt-item").forEach(el => {
    el.classList.toggle("active", el.dataset.id === id);
  });
}

async function deletePatient(id){
  await fetch(`/api/patients/${id}`, {method:"DELETE"});
  
  const local = JSON.parse(localStorage.getItem(LS_KEY) || "[]");
  const filtered = local.filter(p => p.id !== id);
  localStorage.setItem(LS_KEY, JSON.stringify(filtered));

  if(activeId === id){ activeId=null; clearForm(); showEmpty(); }
  loadSidebar();
}

async function saveRecord(data){
  const phone = document.getElementById("phone")?.value || "";
  const nextVisit = document.getElementById("nextVisit")?.value || "";

  const res = await fetch("/api/patients", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({...data, id: activeId, phone, nextVisit})
  });
  const saved = await res.json();
  activeId = saved.id;
  
  const local = JSON.parse(localStorage.getItem(LS_KEY) || "[]");
  const idx = local.findIndex(p => p.id === saved.id);
  if(idx > -1) local[idx] = saved;
  else local.unshift(saved);
  localStorage.setItem(LS_KEY, JSON.stringify(local));

  loadSidebar();
}

function clearForm(){
  ["patientName","age","phone","symptoms","durationVal","medicalHistory","medications","allergies","nextVisit"]
    .forEach(id => {
      const el = document.getElementById(id);
      if(el) el.value = "";
    });
  const sex = document.getElementById("sex");
  if(sex) sex.value = "";
  const unit = document.getElementById("durationUnit");
  if(unit) unit.value = "days";
}

function showEmpty(){
  const panel = document.getElementById("resultsPanel");
  if(panel) {
    panel.innerHTML = `
      <div class="empty-results">
        <div class="big-icon">🩺</div>
        <h3>Ready for diagnosis</h3>
        <p>Fill in patient details and describe symptoms, then hit Run Diagnosis for an instant analysis.</p>
      </div>`;
  }
}

document.addEventListener("DOMContentLoaded", function(){
  const newBtn = document.getElementById("newBtn");
  if(newBtn) {
    newBtn.addEventListener("click", function(){
      activeId = null; 
      clearForm(); 
      showEmpty(); 
      loadSidebar();
    });
  }
  loadSidebar();
});
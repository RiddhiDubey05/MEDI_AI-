let chatHistory = [];
let diagContext = "";

function timeNow(){
  return new Date().toLocaleTimeString("en-IN",{hour:"2-digit",minute:"2-digit"});
}

function addMsg(role, text){
  const box = document.getElementById("chatMsgs");
  const div = document.createElement("div");
  div.className = "msg " + role;
  div.innerHTML = `<div class="msg-bubble">${text.replace(/\n/g,"<br>")}</div><div class="msg-time">${timeNow()}</div>`;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

function setTyping(show){
  document.getElementById("typingIndicator").classList.toggle("show", show);
  const box = document.getElementById("chatMsgs");
  box.scrollTop = box.scrollHeight;
}

async function sendMsg(text){
  if(!text.trim()) return;
  chatHistory.push({role:"user", content: text});
  addMsg("user", text);
  setTyping(true);
  const btn = document.getElementById("sendBtn");
  btn.disabled = true;
  try {
    const res = await fetch("/api/chat", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ message: text, patientContext: diagContext, history: chatHistory })
    });
    const data = await res.json();
    setTyping(false);
    const reply = data.error ? "Sorry, I ran into an error. Please try again." : data.reply;
    chatHistory.push({role:"assistant", content: reply});
    addMsg("bot", reply);
  } catch {
    setTyping(false);
    addMsg("bot", "Network error. Please check your connection.");
    chatHistory.pop();
  } finally {
    btn.disabled = false;
  }
}

function updateContext(results, patientInfo){
  const names = (results.diagnoses||[]).map(d => `${d.name} (${d.probability}%)`).join(", ");
  diagContext = `Patient: ${patientInfo}. Diagnoses: ${names}. Summary: ${results.summary||""}`;
  // Removed automatic message to keep chat history clean for queries
}

document.addEventListener("DOMContentLoaded", function(){
  const input = document.getElementById("chatInput");
  const btn   = document.getElementById("sendBtn");

  btn.addEventListener("click", function(){
    const text = input.value.trim();
    if(!text) return;
    input.value = "";
    input.style.height = "auto";
    sendMsg(text);
  });

  input.addEventListener("keydown", function(e){
    if(e.key === "Enter" && !e.shiftKey){ e.preventDefault(); btn.click(); }
  });

  input.addEventListener("input", function(){
    this.style.height = "auto";
    this.style.height = Math.min(this.scrollHeight, 96) + "px";
  });
});
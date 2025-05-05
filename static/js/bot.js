function updateTime() {
  var now = new Date();
  var hours = now.getHours();
  var minutes = now.getMinutes();
  var timeString = hours + ':' + (minutes < 10 ? '0' + minutes : minutes);
  document.getElementById('clock').textContent = timeString;
}
setInterval(updateTime, 1000);

const msgerForm = document.querySelector(".msger-inputarea");
const msgerInput = document.querySelector(".msger-input");
const msgerChat = document.querySelector(".msger-chat");

const BOT_NAME = "Siri Bot";
const BOT_IMG = "static/img/mhcicon.png";
const PERSON_NAME = "You";
const PERSON_IMG = "static/img/person.png";

// Submit listener
msgerForm.addEventListener("submit", function (event) {
  event.preventDefault();
  const msgText = msgerInput.value;
  if (!msgText.trim()) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";

  fetch(`/get?msg=${encodeURIComponent(msgText)}`)
    .then(res => res.text())
    .then(data => {
      let botMsg = data;
      if (botMsg.includes("[MEDITATE_BTN]")) {
        botMsg = botMsg.replace(
          "[MEDITATE_BTN]",
          `<br><a href="/meditate" target="_blank">
            <button class="meditate-button">Start Guided Meditation</button>
          </a>`
        );
      }
      if (botMsg.includes("[JOURNAL_BTN]")) {
        botMsg = botMsg.replace(
          "[JOURNAL_BTN]",
          `<br><a href="/journal" target="_blank">
            <button class="meditate-button">Start Guided Journaling</button>
          </a>`
        );
      }      
      appendMessage(BOT_NAME, BOT_IMG, "left", botMsg);
    });
});

// Append chat message
function appendMessage(name, img, side, text) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>
        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop = msgerChat.scrollHeight;
}

// Format time
function formatDate(date) {
  const h = date.getHours();
  const m = date.getMinutes();
  return `${h}:${m < 10 ? "0" + m : m}`;
}

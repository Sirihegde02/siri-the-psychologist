const toggleBtn = document.getElementById("toggleBtn");
const bubble = document.getElementById("bubble");
const bubbleText = document.getElementById("bubble-text");
const bgMusic = document.getElementById("bgMusic");

const phases = ["Breathe In", "Hold", "Breathe Out", "Hold"];
let currentPhase = 0;
let count = 1;
let timer = null;
let running = false;

function updateBubble() {
  bubbleText.textContent = `${phases[currentPhase]} ${count}`;
  bubble.style.transform = `scale(${1 + (count / 8)})`;
  count++;

  if (count > 4) {
    count = 1;
    currentPhase = (currentPhase + 1) % phases.length;
  }
}

function startMeditation() {
  if (!running) {
    running = true;
    bgMusic.play();
    toggleBtn.textContent = "Stop Meditation";
    updateBubble();
    timer = setInterval(updateBubble, 1000);
  } else {
    running = false;
    clearInterval(timer);
    bgMusic.pause();
    bgMusic.currentTime = 0;
    toggleBtn.textContent = "Start Meditation";
    bubbleText.textContent = "Start";
    bubble.style.transform = "scale(1)";
    count = 1;
    currentPhase = 0;
  }
}

toggleBtn.addEventListener("click", startMeditation);
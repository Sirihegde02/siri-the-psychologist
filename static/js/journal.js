function generateSuggestion() {
    fetch('/suggest_journal')
      .then(res => res.text())
      .then(text => {
        const current = document.getElementById("journal-text").value;
        document.getElementById("journal-text").value = current + "\n\n" + text;
      });
  }
  
function getNewPrompt() {
    const currentText = document.getElementById("journalBox").value;
    fetch(`/journal?entry=${encodeURIComponent(currentText)}`)
      .then(res => res.text())
      .then(html => {
        document.open();
        document.write(html);
        document.close();
      });
  }
  

  function emailEntry() {
    const entry = document.getElementById("journal-text").value;
    fetch('/email_journal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ entry })
    }).then(res => res.text())
      .then(msg => alert(msg));
  }
  
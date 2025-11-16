document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get("selectedText", (data) => {
    document.getElementById("answer").value = data.selectedText || "";
    document.getElementById("question").focus();
    document.getElementById("tags").value = "Default";
  });

  document.getElementById("submit").addEventListener("click", () => {
    const flashcard = {
      question: document.getElementById("question").value,
      answer: document.getElementById("answer").value,
      tags: document.getElementById("tags").value.split(",").map(t => t.trim())
    };

    fetch("http://localhost:8080", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(flashcard)
    }).then(() => window.close());
  });
});
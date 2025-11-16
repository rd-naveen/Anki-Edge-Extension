chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "createFlashcard",
    title: "Create Anki Flashcard",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "createFlashcard") {
    chrome.storage.local.set({ selectedText: info.selectionText }, () => {
      chrome.action.openPopup();
    });
  }
});
chrome.commands.onCommand.addListener((command) => {
  if (command === "open-popup") {
    chrome.tabs.query({ active: true, currentWindow: true}, (tabs) => {
      chrome.action.openPopup(); // This opens the popup.html
    });
  }
});


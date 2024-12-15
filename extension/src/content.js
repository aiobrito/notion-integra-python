// extension/src/content.js

// Captura o título da página
const pageTitle = document.title;

// Captura a URL da página
const pageUrl = window.location.href;

// ... (lógica para capturar outras informações) ...

// ... (lógica para capturar os dados) ...

// Envia os dados para o popup.js
chrome.runtime.sendMessage({
    action: "capturedData",
    data: {
      title: pageTitle,
      url: pageUrl,
      // ... (outras informações) ...
    }
  });
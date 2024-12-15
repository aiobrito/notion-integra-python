// extension/src/popup.js

document.getElementById('captureButton').addEventListener('click', function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, { action: "captureData" }, function(response) {
        // Tratar a resposta da extensão de conteúdo (content script)
        // Formatar os dados em uma mensagem MCP
        // Enviar a mensagem MCP para o servidor
      });
    });
  });

// extension/src/popup.js

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "capturedData") {
    // Processar os dados recebidos do content script
    console.log("Dados recebidos:", request.data);
    
    // Formatar os dados em uma mensagem MCP
    const mcpMessage = {
      version: "1.0",
      operation: "create", // ou outra operação, como 'update' ou 'delete'
      context: request.data, // Dados capturados pelo content script
      metadata: {
        // Metadados adicionais, se necessário
        // Exemplo: timestamp, usuário, etc.
      }
    };
    
    // Enviar a mensagem MCP para o servidor
    fetch('http://localhost:8000/mcp', { // Substitua pela URL do seu servidor MCP
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(mcpMessage)
    })
    .then(response => response.json())
    .then(data => {
      // Lidar com a resposta do servidor
      console.log('Resposta do servidor:', data);
      // Exibir mensagem de sucesso na interface da extensão
    })
    .catch(error => {
      // Lidar com erros na comunicação com o servidor
      console.error('Erro ao enviar mensagem MCP:', error);
      // Exibir mensagem de erro na interface da extensão
    });
    }
    });
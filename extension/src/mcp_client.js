// extension/src/mcp_client.js
class MCPClient {
    constructor() {
        this.serverUrl = "http://localhost:8000/mcp";
        this.context = {};
    }

    async captureContext(chatData) {
        const message = {
            version: "1.0",
            operation: "capture_context",
            context: {
                source: "chrome_extension",
                timestamp: Date.now(),
                data: chatData
            },
            metadata: {
                browser: "chrome",
                url: window.location.href
            }
        };

        return await this.sendMessage(message);
    }

    async sendMessage(message) {
        const response = await fetch(this.serverUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(message)
        });
        return await response.json();
    }
}
# src/core/mcp_server.py
from typing import Dict, Any
from datetime import datetime
from .notion_client import NotionClient
from .mcp_processor import MCPProcessor  # Importação crítica
from .mcp_types import MCPMessage

# src/core/mcp_server.py
# src/core/mcp_server.py
class MCPServer:
    def __init__(self):
        self.notion = NotionClient()
        
    async def handle_request(self, message: MCPMessage) -> Dict[str, Any]:
        try:
            # Validação enriquecida
            validated = self._validate_message(message)
            
            # Processamento estruturado
            processed = await self._process_message(validated)
            
            # Integração Notion
            await self._sync_to_notion(processed)
            
            return {
                "status": "success",
                "data": processed,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "operation": message.operation
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    def _validate_message(self, message: MCPMessage) -> bool:
        """Validação estrutural da mensagem MCP"""
        required_fields = ["version", "operation", "context"]
        
        return all(hasattr(message, field) for field in required_fields)

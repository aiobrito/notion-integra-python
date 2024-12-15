# src/core/mcp_processor.py
from typing import Dict, Any
from datetime import datetime
from .mcp_types import MCPMessage
from .notion_client import NotionClient

class MCPProcessor:
    def __init__(self):
        self.notion = NotionClient()
        self.context_store: Dict[str, Any] = {}

    def _extract_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações relevantes do contexto"""
        return {
            "content": context.get("content"),
            "type": context.get("type"),
            "metadata": context.get("metadata", {})
        }

    def _enrich_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enriquece dados com metadados adicionais"""
        return {
            **data,
            "processed": True,
            "timestamp": datetime.now().isoformat()
        }

    async def process_context(self, message: MCPMessage) -> Dict[str, Any]:
        """Pipeline principal de processamento"""
        processed_data = self._extract_context(message.context)
        enriched_data = self._enrich_data(processed_data)
        
        await self.notion.create_entry(enriched_data)
        return {"status": "success", "data": enriched_data}
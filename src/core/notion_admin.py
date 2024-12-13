# src/core/notion_admin.py
from collections import defaultdict
from typing import Dict, Any
from .notion_client import NotionClient
from ..config.settings import Settings
class NotionDatabaseAdmin:
    def __init__(self):
        self.client = NotionClient()
        self.database_id = Settings.NOTION_DATABASE_ID
            
    def validate_connection(self) -> Dict[str, Any]:
        """Validação básica de conectividade e estrutura"""
        try:
            response = self.client._make_request(
                method="GET",
                endpoint=f"databases/{self.database_id}"
            )
            
            return {
                "status": "connected",
                "database": {
                    "id": response["id"],
                    "title": response.get("title", [{}])[0].get("text", {}).get("content", "N/A")
                }
            }
        except Exception as e:
            raise Exception(f"Erro de conectividade: {str(e)}")
            # src/core/notion_admin.py
    def get_keywords_snapshot(self) -> Dict[str, Any]:
        """
        Análise estrutural de keywords existentes
        Returns:
            Dict com métricas de uso e metadados
        """
        try:
            response = self.client._make_request(
                method="POST",
                endpoint=f"databases/{self.database_id}/query"
            )
            
            snapshot = {
                "total_pages": len(response.get("results", [])),
                "keywords": defaultdict(int),
                "timestamps": {
                    "first_seen": None,
                    "last_seen": None
                }
            }
            
            for page in response.get("results", []):
                # Análise temporal
                created = page.get("created_time")
                updated = page.get("last_edited_time")
                
                if not snapshot["timestamps"]["first_seen"] or created < snapshot["timestamps"]["first_seen"]:
                    snapshot["timestamps"]["first_seen"] = created
                if not snapshot["timestamps"]["last_seen"] or updated > snapshot["timestamps"]["last_seen"]:
                    snapshot["timestamps"]["last_seen"] = updated
                
                # Contagem de keywords
                keywords = page.get("properties", {}).get("Keywords", {}).get("multi_select", [])
                for kw in keywords:
                    snapshot["keywords"][kw["name"]] += 1
            
            return snapshot
            
        except Exception as e:
            raise Exception(f"Erro na análise: {str(e)}")
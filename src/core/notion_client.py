# src/core/notion_client.py
from typing import Dict, Any
import requests
from ..config.settings import Settings  # Ajuste relativo correto

class NotionClient:
    """Cliente base para integração com Notion API"""
    
    def __init__(self):
        self.api_key = Settings.NOTION_API_KEY
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executa requisições base para a API do Notion"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição Notion: {str(e)}")
    
    def test_connection(self) -> bool:
        """Testa a conectividade com a API do Notion"""
        try:
            database_id = Settings.NOTION_DATABASE_ID
            response = self._make_request(
                method="GET",
                endpoint=f"databases/{database_id}"
            )
            return True if response else False
        except Exception:
            return False

    def get_database(self) -> Dict[str, Any]:
        """Recupera informações do database configurado"""
        database_id = Settings.NOTION_DATABASE_ID
        return self._make_request(
            method="GET",
            endpoint=f"databases/{database_id}"
        )
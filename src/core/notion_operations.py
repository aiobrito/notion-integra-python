# src/core/notion_operations.py
from typing import Dict, List, Any, Optional
from .notion_client import NotionClient
from ..config.settings import Settings

class NotionOperations:
    """Implementação de operações CRUD para Notion Database"""
    
    def __init__(self):
        self.client = NotionClient()
    
    def create_page(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma nova página no database
        Args:
            properties: Propriedades da página a ser criada
        Returns:
            Dict com dados da página criada
        """
        database_id = Settings.NOTION_DATABASE_ID
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        
        return self.client._make_request(
            method="POST",
            endpoint="pages",
            data=data
        )
    
    def read_pages(self, filter_dict: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Recupera páginas do database
        Args:
            filter_dict: Dicionário opcional com filtros
        Returns:
            Lista de páginas encontradas
        """
        database_id = Settings.NOTION_DATABASE_ID
        data = {"filter": filter_dict} if filter_dict else {}
        
        response = self.client._make_request(
            method="POST",
            endpoint=f"databases/{database_id}/query",
            data=data
        )
        
        return response.get("results", [])
    
    def update_page(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza uma página existente
        Args:
            page_id: ID da página a ser atualizada
            properties: Novas propriedades
        Returns:
            Dict com dados atualizados
        """
        return self.client._make_request(
            method="PATCH",
            endpoint=f"pages/{page_id}",
            data={"properties": properties}
        )
    
    def delete_page(self, page_id: str) -> Dict[str, Any]:
        """
        Arquiva uma página (soft delete)
        Args:
            page_id: ID da página a ser arquivada
        Returns:
            Dict com status da operação
        """
        return self.client._make_request(
            method="PATCH",
            endpoint=f"pages/{page_id}",
            data={"archived": True}
        )
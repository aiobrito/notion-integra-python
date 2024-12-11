# src/core/notion_admin.py
from typing import Dict, List, Any, Optional
from .notion_client import NotionClient
from ..config.settings import Settings

class NotionDatabaseAdmin:
    """
    Camada administrativa para gestão estrutural de databases Notion.
    Implementa operações de governança e evolução estrutural.
    """
    
    def __init__(self):
        self.client = NotionClient()
        self.database_id = Settings.NOTION_DATABASE_ID
    
    def get_database_schema(self) -> Dict[str, Any]:
        """Recupera e analisa schema atual do database"""
        try:
            response = self.client._make_request(
                method="GET",
                endpoint=f"databases/{self.database_id}"
            )
            return {
                "id": response["id"],
                "title": response.get("title", [{}])[0].get("text", {}).get("content", "Untitled"),
                "properties": response.get("properties", {})
            }
        except Exception as e:
            raise Exception(f"Erro ao recuperar schema: {str(e)}")
    
    def rename_property(self, old_name: str, new_name: str) -> Dict[str, Any]:
        """
        Renomeia propriedade mantendo configurações
        Args:
            old_name: Nome atual do campo
            new_name: Novo nome desejado
        """
        try:
            schema = self.get_database_schema()
            if old_name not in schema["properties"]:
                raise ValueError(f"Campo {old_name} não encontrado")
                
            property_config = schema["properties"][old_name]
            property_config["name"] = new_name
            
            return self.client._make_request(
                method="PATCH",
                endpoint=f"databases/{self.database_id}",
                data={
                    "properties": {
                        old_name: property_config
                    }
                }
            )
        except Exception as e:
            raise Exception(f"Erro ao renomear propriedade: {str(e)}")
    
    def update_select_options(
        self, 
        property_name: str, 
        options: List[str]
    ) -> Dict[str, Any]:
        """
        Atualiza opções de campos select/multi-select
        Args:
            property_name: Nome do campo
            options: Lista de novas opções
        """
        try:
            schema = self.get_database_schema()
            if property_name not in schema["properties"]:
                raise ValueError(f"Campo {property_name} não encontrado")
                
            field_type = schema["properties"][property_name]["type"]
            if field_type not in ["select", "multi_select"]:
                raise ValueError(f"Campo {property_name} não é do tipo select/multi-select")
                
            config = {
                field_type: {
                    "options": [{"name": option} for option in options]
                }
            }
            
            return self.client._make_request(
                method="PATCH",
                endpoint=f"databases/{self.database_id}",
                data={
                    "properties": {
                        property_name: config
                    }
                }
            )
        except Exception as e:
            raise Exception(f"Erro ao atualizar opções: {str(e)}")
    
    def create_related_database(
        self, 
        title: str, 
        properties: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Cria novo database com relação ao atual
        Args:
            title: Título do novo database
            properties: Configuração de propriedades
        """
        try:
            base_properties = {
                "Name": {"title": {}},
                "Related": {
                    "relation": {
                        "database_id": self.database_id
                    }
                }
            }
            
            if properties:
                base_properties.update(properties)
            
            return self.client._make_request(
                method="POST",
                endpoint="databases",
                data={
                    "title": [{"text": {"content": title}}],
                    "properties": base_properties
                }
            )
        except Exception as e:
            raise Exception(f"Erro ao criar database: {str(e)}")
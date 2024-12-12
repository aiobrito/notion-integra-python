# src/core/notion_admin.py
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
from .notion_client import NotionClient
from ..config.settings import Settings
from .validators import InputValidator
from .rate_limiter import rate_limit

# src/core/notion_admin.py

class NotionDatabaseAdmin:
    def __init__(self):
        self.client = NotionClient()
        self.database_id = Settings.NOTION_DATABASE_ID
        self.taxonomy = {
            "tech": {
                "terms": ["API", "VSCode", "JavaScript", "Python", "Integration"],
                "synonyms": {
                    "VS Code": "VSCode",
                    "VS": "VSCode",
                    "JS": "JavaScript",
                    "Node": "JavaScript",
                    "py": "Python"
                },
                "max_terms": 8
            },
            "ai_ml": {
                "terms": ["GPT", "AI", "ML", "Prompt", "LLM", "Gemini"],
                "synonyms": {
                    "ChatGPT": "GPT",
                    "Chat GPT": "GPT",
                    "Artificial Intelligence": "AI",
                    "Machine Learning": "ML",
                    "Large Language Model": "LLM"
                },
                "max_terms": 6
            },
            "process": {
                "terms": ["Development", "Testing", "CI/CD", "Automation"],
                "synonyms": {
                    "Dev": "Development",
                    "Test": "Testing",
                    "Pipeline": "CI/CD",
                    "Auto": "Automation"
                },
                "max_terms": 5
            },
            "management": {
                "terms": ["Documentation", "Security", "Optimization"],
                "synonyms": {
                    "Docs": "Documentation",
                    "Doc": "Documentation",
                    "Secure": "Security",
                    "Optim": "Optimization"
                },
                "max_terms": 5
            }
        }
    """
    Camada administrativa para gestão estrutural de databases Notion.
    Implementa operações de governança e evolução estrutural.
    """    
    def __init__(self):
        self.client = NotionClient()
        self.database_id = Settings.NOTION_DATABASE_ID
    
    @rate_limit(calls=5, period=60)
    def validate_tag(self, new_tag: str) -> Dict[str, Any]:
        InputValidator.validate_tag(new_tag)
    
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
    
    def get_multiselect_options(self) -> Dict[str, Any]:
        """Recupera configuração atual do Multi-select"""
        try:
            schema = self.get_database_schema()
            multi_select = schema['properties'].get('Multi-select', {})
            options = multi_select.get('multi_select', {}).get('options', [])
            
            return {
                "total": len(options),
                "options": [opt['name'] for opt in options],
                "raw_config": multi_select
            }
        except Exception as e:
            raise Exception(f"Erro ao recuperar opções: {str(e)}")
    
    @rate_limit(calls=10, period=60)
    def validate_tag(self, new_tag: str) -> Dict[str, Any]:
        """
        Valida tag contra existentes e sugere similares
        Args:
            new_tag: Tag proposta para inserção
        Returns:
            Dict com status de validação e sugestões
        """
        try:
            options = self.get_multiselect_options()
            existing = [tag.lower() for tag in options['options']]
            new_tag_lower = new_tag.lower()
            
            similar = [
                tag for tag in options['options']
                if (new_tag_lower in tag.lower() or 
                    tag.lower() in new_tag_lower)
            ]
            
            return {
                "tag": new_tag,
                "exists": new_tag_lower in existing,
                "similar_count": len(similar),
                "suggestions": similar
            }
        except Exception as e:
            raise Exception(f"Erro na validação: {str(e)}")
    def suggest_tags(self, partial: str) -> List[str]:
        """
        Sugere tags baseado em texto parcial
        Args:
            partial: Texto para busca
        Returns:
            Lista de tags sugeridas
        """
        try:
            if len(partial) < 2:
                return []
                
            options = self.get_multiselect_options()
            partial_lower = partial.lower()
            
            return [
                tag for tag in options['options']
                if partial_lower in tag.lower()
            ]
        except Exception as e:
            raise Exception(f"Erro na sugestão: {str(e)}")
    
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
        # src/core/notion_admin.py - Ajustes Críticos

def normalize_term(self, term: str) -> Tuple[str, str]:
    """
    Normalização hierárquica com análise categórica profunda
    """
    term_clean = term.strip()
    term_lower = term_clean.lower()
    
    # Otimização da categorização
    direct_matches = {
        "VSCode": "tech",
        "GPT": "ai_ml",
        "Documentation": "management",
        "Testing": "process"
    }
    
    if term_clean in direct_matches:
        return term_clean, direct_matches[term_clean]
        
    # Pattern matching avançado
    pattern_rules = [
        (r".*js$", "JavaScript", "tech"),
        (r"py.*", "Python", "tech"),
        (r".*gpt.*", "GPT", "ai_ml"),
        (r".*test.*", "Testing", "process")
    ]
    
    return self._apply_pattern_rules(term_clean, pattern_rules)
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
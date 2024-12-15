# src/core/mcp_types.py
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class MCPMessage:
    """Define estrutura base de mensagens MCP"""
    version: str
    operation: str
    context: Dict[str, Any]
    metadata: Dict[str, Any]
class MessageValidator:
    def __init__(self, validation_rules=None):
        self.rules = validation_rules or self._default_validation_rules()
    
    def _default_validation_rules(self):
        return {
            'schema_integrity': True,
            'context_relevance': 0.7,  # Limiar de relevância contextual
            'max_context_depth': 3,
            'allowed_types': ['text', 'structured', 'semantic']
        },
    
    def validate(self, message):
        """
        Valida mensagem segundo regras definidas
        Retorna dicionário de validação detalhado
        """
        validation_result = {
            'is_valid': True,
            'checks': {}
        }
        
        # Implementação de validações específicas
        return validation_result
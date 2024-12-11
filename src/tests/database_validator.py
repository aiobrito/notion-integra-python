# src/tests/database_validator.py
import sys
from pathlib import Path
from src.core.notion_operations import NotionOperations
from src.config.settings import Settings

# Setup do path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

def validate_database_structure():
    """
    Analisa e valida a estrutura do database Notion
    retornando suas propriedades e tipos
    """
    try:
        ops = NotionOperations()
        
        print("\n=== Validação de Estrutura do Database ===")
        print(f"Database ID: {Settings.NOTION_DATABASE_ID}")
        
        # Recupera metadados do database
        database = ops.client._make_request(
            method="GET",
            endpoint=f"databases/{Settings.NOTION_DATABASE_ID}"
        )
        
        print("\nPropriedades Encontradas:")
        for prop_name, details in database.get("properties", {}).items():
            prop_type = details.get("type", "unknown")
            print(f"- {prop_name} (tipo: {prop_type})")
            
        return database.get("properties", {})
    
    except Exception as e:
        print(f"\n✗ Erro na validação: {str(e)}")
        return None

if __name__ == "__main__":
    print("\n=== Iniciando Validação do Database Notion ===")
    properties = validate_database_structure()
    
    if properties:
        print("\n✓ Validação concluída com sucesso")
    else:
        print("\n✗ Falha na validação")
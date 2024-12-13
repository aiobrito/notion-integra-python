# src/tests/test_operations.py
# import os #nao necessario
import sys
#from pathlib import Path# Import utilizando caminho absoluto
from src.core.notion_operations import NotionOperations
from src.core.notion_admin import NotionDatabaseAdmin

# src/tests/test_operations.py

def test_crud_flow():
    """Validação do fluxo CRUD com análise de integridade"""
    print("\n=== Validação de Operações CRUD ===")
    ops = NotionOperations()
    
    test_entry = {
        "name": "Segurança para Agentes AI ChatGPT",
        "url": "https://chat.openai.com/security",
        "desc": "Diretrizes e implementações de segurança para agentes AI",
        "keywords": ["Security", "AI", "Implementation", "Guidelines"]
    }
    
    try:
        # CREATE
        print("\n1. Testando Criação...")
        new_page = ops.create_entry(test_entry)
        page_id = new_page['id']
        print(f"✓ Página criada: {page_id}")
        
        # BLOCKS
        print("\n2. Adicionando Blocos...")
        blocks = ops.create_blocks(page_id)
        print(f"✓ Blocos criados: {len(blocks.get('results', []))}")
        
        # ENHANCE
        print("\n3. Enriquecimento...")
        enhanced = ops.enhance_entry(page_id, test_entry['url'])
        print(f"✓ Keywords: {len(enhanced['properties']['Keywords']['multi_select'])}")
        
        return True
    except Exception as e:
        print(f"✗ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_crud_flow()
    print(f"\nStatus Final: {'✓ Sucesso' if success else '✗ Falha'}")
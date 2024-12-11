# src/tests/test_operations.py
# import os #nao necessario
import sys
from pathlib import Path# Import utilizando caminho absoluto
from src.core.notion_operations import NotionOperations

# Configuração de path otimizada
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

def main():
    try:
        ops = NotionOperations()
        print("\nTestando leitura de páginas...")
        pages = ops.read_pages()
        print(f"✓ {len(pages)} páginas encontradas")
        return True
    except Exception as e:
        print(f"✗ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    print("\nStatus:", "✓ Sucesso" if success else "✗ Falha")
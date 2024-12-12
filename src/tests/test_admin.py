# src/tests/test_admin.py
from src.core.notion_admin import NotionDatabaseAdmin

def test_connection():
    """Teste base já implementado e funcionando"""
    admin = NotionDatabaseAdmin()
    print("\n=== Validação de Conectividade ===")
    status = admin.validate_connection()
    print(f"✓ Conectado ao database: {status['database']['title']}")
    print(f"✓ ID: {status['database']['id']}")
    return True

def test_keywords_snapshot():
    """Validação estrutural de keywords"""
    admin = NotionDatabaseAdmin()
    
    print("\n=== Análise Estrutural de Keywords ===")
    try:
        snapshot = admin.get_keywords_snapshot()
        
        print("\nBase de Dados:")
        print(f"▸ Total de Páginas: {snapshot['total_pages']}")
        
        print("\nDistribuição de Keywords:")
        for kw, count in sorted(snapshot['keywords'].items(), 
                              key=lambda x: x[1], reverse=True):
            print(f"▸ {kw}: {count} {'uso' if count == 1 else 'usos'}")
        
        if snapshot['timestamps']['first_seen']:
            print("\nLinha do Tempo:")
            print(f"▸ Primeiro Registro: {snapshot['timestamps']['first_seen']}")
            print(f"▸ Última Atualização: {snapshot['timestamps']['last_seen']}")
            
        return True
        
    except Exception as e:
        print(f"✗ Erro: {str(e)}")
        return False
def main():
    """Função principal de execução"""
    connection = test_connection()
    content = test_keywords_snapshot()
    print(f"\nStatus Final: {'✓ Sucesso' if all([connection, content]) else '✗ Falha'}")
    
if __name__ == "__main__":
    success = test_keywords_snapshot()
    print(f"\nStatus: {'✓ Sucesso' if success else '✗ Falha'}")
from src.core.notion_client import NotionClient

def main():
    client = NotionClient()
    
    print("Testando conexão com Notion...")
    if client.test_connection():
        print("✓ Conexão estabelecida com sucesso!")
        
        print("\nRecuperando informações do database...")
        database = client.get_database()
        print(f"✓ Database título: {database.get('title', [{}])[0].get('plain_text', 'N/A')}")
    else:
        print("✗ Falha na conexão com Notion")

if __name__ == "__main__":
    main()
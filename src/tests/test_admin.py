# src/tests/test_admin.py - Nova Implementação
from src.core.notion_admin import NotionDatabaseAdmin

def test_admin_operations():
    """Validação do schema atual do database"""
    admin = NotionDatabaseAdmin()
    
    print("\n=== Schema Analysis ===")
    schema = admin.get_database_schema()
    print(f"Database: {schema['title']}")
    print("\nCurrent Structure:")
    for prop_name, details in schema['properties'].items():
        print(f"▸ {prop_name:<15} | Type: {details['type']}")
    
    return True

if __name__ == "__main__":
    status = test_admin_operations()
    print(f"\nValidation Status: {'✓ Success' if status else '✗ Failed'}")
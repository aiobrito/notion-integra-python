# src/tests/test_notion_admin.py
import pytest
from unittest.mock import Mock, patch
from src.core.notion_admin import NotionDatabaseAdmin

@pytest.fixture
def notion_admin():
    return NotionDatabaseAdmin()

@pytest.fixture
def mock_response():
    return {
        "id": "test-db",
        "title": [{"text": {"content": "Test DB"}}],
        "properties": {
            "Tags": {
                "type": "multi_select",
                "multi_select": {"options": []}
            }
        }
    }

def test_get_database_schema(notion_admin, mock_response):
    with patch('src.core.notion_client.NotionClient._make_request') as mock_request:
        mock_request.return_value = mock_response
        schema = notion_admin.get_database_schema()
        assert schema["id"] == "test-db"
        assert "properties" in schema
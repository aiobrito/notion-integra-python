# tests/conftest.py
import pytest
from src.core.notion_admin import NotionDatabaseAdmin

@pytest.fixture
def mock_schema():
    return {
        "id": "test-db-id",
        "title": [{"text": {"content": "Test Database"}}],
        "properties": {
            "Multi-select": {
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {"name": "Python"},
                        {"name": "JavaScript"}
                    ]
                }
            }
        }
    }

@pytest.fixture
def notion_admin(mocker):
    admin = NotionDatabaseAdmin()
    mocker.patch.object(admin.client, '_make_request')
    return admin
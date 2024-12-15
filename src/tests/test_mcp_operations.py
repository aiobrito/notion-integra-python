# src/tests/test_mcp_operations.py
import pytest
from typing import Dict, Any
from src.core.mcp_types import MCPMessage
from src.core.mcp_server import MCPServer

@pytest.mark.asyncio
async def test_create_operation():
    """Testa operação CREATE no Notion via MCP"""
    server = MCPServer()
    
    message = MCPMessage(
        version="1.0",
        operation="create",
        context={
            "title": "Test Entry",
            "content": "Test Content",
            "tags": ["test", "mcp"]
        },
        metadata={"source": "test"}
    )
    
    response = await server.handle_request(message)
    assert response["status"] == "success"
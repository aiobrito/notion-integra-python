# src/tests/test_mcp.py
import pytest
from ..core.mcp_types import MCPMessage
from ..core.mcp_server import MCPServer

@pytest.mark.asyncio
async def test_mcp_flow():
    """Validação do fluxo MCP básico"""
    server = MCPServer()
    
    test_message = MCPMessage(
        version="1.0",
        operation="capture_context",
        context={
            "content": "Test message",
            "type": "chat"
        },
        metadata={
            "source": "test"
        }
    )
    
    response = await server.handle_request(test_message)
    assert response["status"] == "success"

# src/tests/test_mcp_validation.py
import pytest
from src.core.mcp_types import MCPMessage
from src.core.mcp_server import MCPServer

@pytest.mark.asyncio
async def test_invalid_message():
    """Testa validação de mensagens inválidas"""
    server = MCPServer()
    
    invalid_message = MCPMessage(
        version="1.0",
        operation="invalid_op",
        context={},
        metadata={}
    )
    
    response = await server.handle_request(invalid_message)
    assert response["status"] == "error"
# src/tests/test_mcp_validation.py
@pytest.mark.asyncio
class TestMCPValidation:
    async def test_invalid_message(self):
        """Testa validação de mensagens inválidas"""
        invalid_message = MCPMessage(
            version="1.0",
            operation="invalid_op",
            context={},
            metadata={}
        )
        # Implementar validação
# src/tests/test_crud_operations.py
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Tuple
from src.core.notion_operations import NotionOperations
# from src.config.settings import Settings

# Setup do path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))



class NotionTestSuite:
    """
    Suite de testes otimizada para Notion API
    Implementa padrões de validação e feedback estruturado
    """
    
    def __init__(self):
        self.ops = NotionOperations()
        self.test_reference = datetime.now().strftime('TEST-%Y%m%d-%H%M%S')
        self.page_id = None
    
    def execute_operation(self, operation: str, func, *args) -> Tuple[bool, Any]:
        """
        Executor padronizado de operações com feedback estruturado
        """
        try:
            result = func(*args)
            return True, result
        except Exception as e:
            print(f"✗ Erro em {operation}: {str(e)}")
            return False, None
    
    def validate_create(self) -> bool:
        """Teste de criação com payload otimizado"""
        print("\n1. CREATE Operation")
        
        create_data = {
            "Nome": {
                "title": [{"text": {"content": f"Test Entry - {self.test_reference}"}}]
            },
            "Desc": {
                "rich_text": [{"text": {"content": "Validação automatizada"}}]
            }
        }
        
        success, response = self.execute_operation("CREATE", self.ops.create_page, create_data)
        if success:
            self.page_id = response["id"]
            print("✓ Página criada:", self.page_id)
            return True
        return False
    
    def validate_read(self) -> bool:
        """Teste de leitura otimizado - single execution"""
        print("\n2. READ Operation")
        success, pages = self.execute_operation("READ", self.ops.read_pages)
        if success:
            print(f"✓ Páginas recuperadas: {len(pages)}")
            return True
        return False
    
    def validate_update(self) -> bool:
        """Teste de atualização com validação de estado"""
        if not self.page_id:
            print("✗ UPDATE: ID não disponível")
            return False
            
        print("\n3. UPDATE Operation")
        update_data = {
            "Nome": {
                "title": [{"text": {"content": f"Updated - {self.test_reference}"}}]
            }
        }
        
        success, _ = self.execute_operation("UPDATE", 
                                          self.ops.update_page,
                                          self.page_id, 
                                          update_data)
        if success:
            print("✓ Atualização concluída")
            return True
        return False
    
    def validate_delete(self) -> bool:
        """Teste de deleção (archive) com validação de estado"""
        if not self.page_id:
            print("✗ DELETE: ID não disponível")
            return False
            
        print("\n4. DELETE Operation")
        success, _ = self.execute_operation("DELETE", 
                                          self.ops.delete_page,
                                          self.page_id)
        if success:
            print("✓ Arquivo concluído")
            return True
        return False
    
    def run_suite(self) -> bool:
        """Execução sequencial otimizada da suite de testes"""
        operations = [
            self.validate_create,
            self.validate_read,
            self.validate_update,
            self.validate_delete
        ]
        
        results = []
        for operation in operations:
            results.append(operation())
            if not results[-1]:
                break
                
        return all(results)

def main():
    """Ponto de entrada com métricas de execução"""
    print("\n=== Notion CRUD Validation Suite ===")
    
    suite = NotionTestSuite()
    start_time = datetime.now()
    success = suite.run_suite()
    execution_time = (datetime.now() - start_time).total_seconds()
    
    print(f"\nExecution Time: {execution_time:.2f}s")
    print(f"Status: {'✓ Success' if success else '✗ Failed'}")
    
    return 0 if success else 1

if __name__ == "__main__":
    main()
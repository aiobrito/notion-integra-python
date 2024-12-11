# test_config.py
from src.config.settings import Settings

def test_env():
    Settings.validate()
    print("Configuração validada com sucesso!")

if __name__ == "__main__":
    test_env()
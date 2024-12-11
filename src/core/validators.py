# src/core/validators.py
from typing import Any, Dict

class InputValidator:
    @staticmethod
    def validate_tag(tag: str) -> None:
        if not isinstance(tag, str):
            raise ValueError("Tag deve ser string")
        if len(tag.strip()) < 2:
            raise ValueError("Tag muito curta")
        if len(tag) > 50:
            raise ValueError("Tag muito longa")
        if not all(c.isalnum() or c in '-_' for c in tag):
            raise ValueError("Caracteres inválidos na tag")
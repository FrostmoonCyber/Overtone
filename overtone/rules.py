import re
from dataclasses import dataclass
from typing import List, Pattern


@dataclass
class DetectionRule:
    """Represent a detection rule based on regular expressions."""
    name: str
    pattern: Pattern
    token_label: str
    description: str


class RuleRegistry:
    """Colection and detection rule management for Overtone."""

    def __init__(self):
        self.rules: List[DetectionRule] = []
        self._load_default_rules()

    def _load_default_rules(self):
        # -----------------------------------------------------------------
        # 1. SWISS IDENTIFIERS (Swiss Regulatory Alignment - nLPD/FADP)
        # -----------------------------------------------------------------
        
        # Número AHV/AVS (NVS): Formato 756.XXXX.XXXX.XX
        self.rules.append(
            DetectionRule(
                name="swiss_ahv",
                pattern=re.compile(r"\b756\.\d{4}\.\d{4}\.\d{2}\b"),
                token_label="SWISS_AHV",
                description="Número de seguridad social suizo (AHV/AVS)"
            )
        )

        # Código IBAN Suizo: CHXX XXXX XXXX XXXX XXXX X
        self.rules.append(
            DetectionRule(
                name="swiss_iban",
                pattern=re.compile(r"\bCH\d{2}[ ]?(?:\d{4}[ ]?){4}\d?\b", re.IGNORECASE),
                token_label="SWISS_IBAN",
                description="Número de cuenta bancaria IBAN suizo"
            )
        )

        # -----------------------------------------------------------------
        # 2. INFORMACIÓN DE IDENTIFICACIÓN PERSONAL (PII Genérica)
        # -----------------------------------------------------------------

        # Correo electrónico
        self.rules.append(
            DetectionRule(
                name="email",
                pattern=re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
                token_label="EMAIL",
                description="Dirección de correo electrónico"
            )
        )

        # Número de teléfono (Formatos internacionales y suizos habituales)
        self.rules.append(
            DetectionRule(
                name="phone_number",
                pattern=re.compile(r"(?:\+41|0041|0)\s?\(?0?\)?\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}\b"),
                token_label="PHONE",
                description="Número de teléfono formato suizo / internacional"
            )
        )

        # Tarjetas de crédito (Visa, Mastercard, etc. simplificado)
        self.rules.append(
            DetectionRule(
                name="credit_card",
                pattern=re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
                token_label="CREDIT_CARD",
                description="Número de tarjeta de crédito/débito"
            )
        )

    def get_rules(self) -> List[DetectionRule]:
        """Devuelve la lista completa de reglas registradas."""
        return self.rules


if __name__ == "__main__":
    # Prueba rápida de funcionamiento
    registry = RuleRegistry()
    print(f"✅ Se han cargado {len(registry.get_rules())} reglas por defecto en Overtone:")
    for rule in registry.get_rules():
        print(f" - [{rule.token_label}] {rule.name}: {rule.description}")
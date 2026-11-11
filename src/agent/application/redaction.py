"""Enmascara datos personales antes de indexar y detecta fugas en las respuestas."""

import re

CARD_NUMBER = re.compile(r"\b(?:\d[ -]?){12,18}\d\b")
DNI = re.compile(r"\b\d{8}\b")


def redact_personal_data(text: str) -> str:
    # Primero las tarjetas: pueden contener grupos de ocho dígitos que parecen DNI.
    return DNI.sub("[DNI]", CARD_NUMBER.sub("[TARJETA]", text))


def contains_personal_data(text: str) -> bool:
    return bool(CARD_NUMBER.search(text) or DNI.search(text))

from enum import StrEnum

class Alephbet:
    LETTERS = 'אבגדהוזחטיכלמנסעפצקרשת'
    FINALS = 'ךםןףץ'
    LETTERS_WITH_FINALS = LETTERS + FINALS
    FINALS_MAPPING = {
        'ך': 'כ',
        'ם': 'מ',
        'ן': 'נ',
        'ף': 'פ',
        'ץ': 'צ',
    }

class Niqqud(StrEnum):
    PATAH = '\u05B7'
    KAMATZ = '\u05B8'
    TZEIREI = '\u05B5'
    SEGOL = '\u05B6'
    HIRIQ = '\u05B4'
    HOLAM = '\u05B9'
    QUBUTZ = '\u05BB'
    SHVA = '\u05B0'
    HATAF_PATAH = '\u05B2'
    HATAF_SEGOL = '\u05B1'
    HATAF_KAMATZ = '\u05B3'
    DAGESH = '\u05BC'
    SHIN_DOT_RIGHT = '\u05C1'
    SHIN_DOT_LEFT = '\u05C2'

    @staticmethod
    def to_list():
        return [(n.value, n.name) for n in Niqqud]

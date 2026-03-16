from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ParsedInstruction:
    """Normalized target extracted from a natural-language instruction."""

    raw_text: str
    target_object: str
    relation: Optional[str] = None
    reference_object: Optional[str] = None


class LanguageParser:
    """Rule-based parser for a minimal ObjectNav instruction grammar.

    Supported examples:
    - "go to the chair"
    - "move to desk"
    - "go to the chair near the door"
    - "move to the desk by window"
    """

    _RELATION_KEYWORDS = {
        "near": "near",
        "by": "near",
        "next to": "near",
    }

    _LEADING_PREFIXES = (
        "go to ",
        "move to ",
        "navigate to ",
        "find ",
    )

    def parse(self, instruction: str) -> ParsedInstruction:
        text = " ".join(instruction.strip().lower().split())
        if not text:
            raise ValueError("Instruction cannot be empty.")

        for prefix in self._LEADING_PREFIXES:
            if text.startswith(prefix):
                text = text[len(prefix) :]
                break

        text = self._drop_article(text)

        relation = None
        relation_start = -1
        relation_kw = None
        for candidate, normalized in self._RELATION_KEYWORDS.items():
            needle = f" {candidate} "
            idx = text.find(needle)
            if idx != -1 and (relation_start == -1 or idx < relation_start):
                relation_start = idx
                relation = normalized
                relation_kw = candidate

        if relation is None:
            target = self._drop_article(text)
            if not target:
                raise ValueError(f"Could not parse target object from instruction: {instruction}")
            return ParsedInstruction(raw_text=instruction, target_object=target)

        target = self._drop_article(text[:relation_start])
        reference = self._drop_article(text[relation_start + len(relation_kw) + 2 :])
        if not target or not reference:
            raise ValueError(f"Incomplete relational instruction: {instruction}")

        return ParsedInstruction(
            raw_text=instruction,
            target_object=target,
            relation=relation,
            reference_object=reference,
        )

    @staticmethod
    def _drop_article(text: str) -> str:
        text = text.strip()
        for article in ("the ", "a ", "an "):
            if text.startswith(article):
                return text[len(article) :].strip()
        return text

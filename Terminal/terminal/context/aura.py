from typing import Any

__all__ = [
    "Aura",
]


class Aura:
    def __init__(self, spell: dict[str, Any]) -> None:
        """
        aura的结构如下: 
        auraData = {
            "title": icon_cell.title,
            "remain": remain_cell.remaining,
            "color_string": type_cell.color_string,
            "type": COLOR_MAP["SPELL_TYPE"].get(type_cell.color_string, "UNKNOWN"),
            "count": count_cell,
        }
        """
        self.spell = spell

    def __str__(self) -> str:
        return self.spell["title"]

    @property
    def title(self) -> str:
        return self.spell["title"]

    @property
    def remain(self) -> float:
        return float(self.spell.get("remain", 999.0))

    @property
    def type(self) -> str:
        return self.spell.get("type", "UNKNOWN")

    @property
    def count(self) -> int:
        return self.spell.get("count", 1)

    @property
    def color_string(self) -> str:
        return self.spell.get("color_string", "0,0,0")

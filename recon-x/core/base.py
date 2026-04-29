# core/base.py — Abstract base class all modules inherit from

from abc import ABC, abstractmethod
from core.config import C


class BaseModule(ABC):
    """Every tool module subclasses this."""

    # Override in subclass
    NAME  : str = "Module"
    COLOR : str = C.CYAN
    DESC  : str = ""

    def header(self) -> None:
        """Print a small section header before running."""
        bar = "─" * 50
        print(f"\n{self.COLOR}{C.BOLD}{bar}")
        print(f"  ◆ {self.NAME}")
        if self.DESC:
            print(f"  {C.DIM}{self.DESC}{C.RESET}")
        print(f"{self.COLOR}{bar}{C.RESET}\n")

    @abstractmethod
    def run(self) -> None:
        """Entry point called by the menu."""
        ...

    # ── shared helpers ──────────────────────────────────────────────────────

    @staticmethod
    def prompt(label: str, color: str = C.CYAN) -> str:
        """Styled input prompt; strips whitespace."""
        return input(f"{color}{C.BOLD}  [{label}] ▶ {C.RESET}").strip()

    @staticmethod
    def ok(msg: str) -> None:
        print(f"  {C.OK}✔  {msg}{C.RESET}")

    @staticmethod
    def warn(msg: str) -> None:
        print(f"  {C.WARN}⚠  {msg}{C.RESET}")

    @staticmethod
    def err(msg: str) -> None:
        print(f"  {C.ERR}✘  {msg}{C.RESET}")

    @staticmethod
    def info(msg: str) -> None:
        print(f"  {C.INFO}ℹ  {msg}{C.RESET}")

    @staticmethod
    def kv(key: str, value: str, key_color: str = C.CYAN) -> None:
        """Print a key/value pair with aligned formatting."""
        print(f"  {key_color}{key:<22}{C.RESET}{value}")

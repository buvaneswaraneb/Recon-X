#!/usr/bin/env python3
# main.py — RECON-X entry point

import sys
from utils.helpers import print_banner, print_menu, pause, clear
from modules import ALL_MODULES
from core.config import C

EXIT_CHOICE = 13


def main() -> None:
    while True:
        print_banner()
        print_menu()

        try:
            raw = input(f"  {C.CYAN}{C.BOLD}recon-x{C.RESET} {C.DIM}▶{C.RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {C.DIM}Interrupted. Goodbye.{C.RESET}\n")
            sys.exit(0)

        if not raw:
            continue

        if not raw.isdigit():
            print(f"\n  {C.ERR}✘  Invalid choice — enter a number (1–{EXIT_CHOICE}).{C.RESET}")
            pause()
            continue

        choice = int(raw)

        if choice == EXIT_CHOICE:
            clear()
            print(f"\n  {C.CYAN}{C.BOLD}RECON-X{C.RESET}  {C.DIM}— session ended. Stay safe.{C.RESET}\n")
            sys.exit(0)

        if choice < 1 or choice > EXIT_CHOICE:
            print(f"\n  {C.ERR}✘  Choice out of range (1–{EXIT_CHOICE}).{C.RESET}")
            pause()
            continue

        # Instantiate and run the selected module
        module_class = ALL_MODULES[choice - 1]
        module = module_class()
        try:
            module.run()
        except KeyboardInterrupt:
            print(f"\n\n  {C.WARN}⚠  Module interrupted.{C.RESET}")
            pause()
        except Exception as e:
            print(f"\n  {C.ERR}✘  Unexpected error: {e}{C.RESET}")
            pause()


if __name__ == "__main__":
    main()

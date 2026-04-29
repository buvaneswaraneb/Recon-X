# core/config.py — Color palette, constants, and shared config

TOOL_NAME    = "RECON-X"
TOOL_VERSION = "1.0.0"
TOOL_AUTHOR  = "github.com/your-handle"

# ANSI colors — each module picks its own accent
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Palette
    BLACK   = "\033[30m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    ORANGE  = "\033[38;5;208m"
    PINK    = "\033[38;5;213m"
    LIME    = "\033[38;5;154m"
    TEAL    = "\033[38;5;45m"
    PURPLE  = "\033[38;5;135m"

    # Semantic
    OK      = "\033[92m"   # green
    WARN    = "\033[93m"   # yellow
    ERR     = "\033[91m"   # red
    INFO    = "\033[96m"   # cyan

# Menu color assignments per option index (1-13)
MENU_COLORS = [
    C.CYAN,    # 1  IP Lookup
    C.GREEN,   # 2  Domain Lookup
    C.YELLOW,  # 3  Port Scanner
    C.BLUE,    # 4  DNS Lookup
    C.MAGENTA, # 5  OSINT Search
    C.ORANGE,  # 6  System Info
    C.TEAL,    # 7  Ping Test
    C.PINK,    # 8  Header Grabber
    C.LIME,    # 9  SSL Checker
    C.PURPLE,  # 10 Subdomain Finder
    C.RED,     # 11 Username Search
    C.WHITE,   # 12 Directory Bruteforce
    C.DIM,     # 13 Exit
]

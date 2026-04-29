# modules/__init__.py — Central registry; import order matches menu order

from modules.ip_lookup        import IPLookup
from modules.domain_lookup    import DomainLookup
from modules.port_scanner     import PortScanner
from modules.dns_lookup       import DNSLookup
from modules.osint_search     import OSINTSearch
from modules.system_info      import SystemInfo
from modules.ping_test        import PingTest
from modules.header_grabber   import HeaderGrabber
from modules.ssl_checker      import SSLChecker
from modules.subdomain_finder import SubdomainFinder
from modules.username_search  import UsernameSearch
from modules.dir_bruteforce   import DirBruteforce

# Ordered list consumed by main.py menu router
ALL_MODULES = [
    IPLookup,
    DomainLookup,
    PortScanner,
    DNSLookup,
    OSINTSearch,
    SystemInfo,
    PingTest,
    HeaderGrabber,
    SSLChecker,
    SubdomainFinder,
    UsernameSearch,
    DirBruteforce,
]

import hashlib
from typing import Iterable

from app.models.payload import PayloadSource
from app.services.payload.payload_url_presentation import (
    derive_payload_presentation,
    normalize_payload_url,
)

REMOTE_PAYLOAD_CATALOG_SCHEMA_VERSION = 1
REMOTE_PAYLOAD_CATALOG_APP = "sendpp"
REMOTE_PAYLOAD_CATALOG_URL = "https://raw.githubusercontent.com/ps4macedo/sendpp/main/catalogs/payload_catalog.json"


# -----------------------------------------------------------------------------
# CATÁLOGO DE PAYLOADS
# -----------------------------------------------------------------------------
# Para adicionar um payload comum à lista, adicione SOMENTE a URL aqui.
# Nome, chave e versão são derivados automaticamente do próprio link.
# Não existe tabela paralela de nomes/versões.
# -----------------------------------------------------------------------------
PAYLOAD_URLS = (
    "https://github.com/ps4macedo/instalador-host-psm-poop2jb/releases/download/v1.2.0/Host-PSM-pooP2JB-v1.2.0-instala-pldmgr.elf",
    "https://github.com/ps4macedo/instalador-host-psm-poop2jb/releases/download/v1.2.0/Host-PSM-pooP2JB-v1.2.0-instala-pldmgr-en.elf",
    "https://github.com/ps4macedo/instalador-host-psm-poop2jb/releases/download/v1.2.0/Host-PSM-pooP2JB-v1.2.0-instala-onionhen.elf",
    "https://github.com/ps4macedo/instalador-host-psm-poop2jb/releases/download/v1.2.0/Host-PSM-pooP2JB-v1.2.0-instala-onionhen-en.elf",
    "https://github.com/earthonion/np-fake-signin/releases/download/1.1/np-fake-signin-ps5.elf",
    "https://github.com/EchoStretch/kstuff-lite/releases/download/v1.06/kstuff.elf",
    "https://github.com/drakmor/ShadowMountPlus/releases/download/1.6test11/ShadowMountPlus_1.6test11.zip",
    "https://github.com/ps5-payload-dev/ftpsrv/releases/download/v0.20/ftpsrv-ps5.elf",
    "https://github.com/drakmor/ftpsrv/releases/download/1.15-ng-beta8/ftpsrv-ps5.elf",
    "https://github.com/itsPLK/ps5-payload-manager/releases/download/v0.1.1/pldmgr-v0.1.1.elf",
    "https://github.com/tsuramatsu1/apr-emu-updater/releases/download/v1.5.1/apr_emu_updater.elf",
    "https://github.com/matem6/P2JB-Y2JB-Porting/releases/download/2.6/p2jb.js",
    "https://github.com/Gezine/Y2JB/raw/main/payloads/lapse.js",
    "https://github.com/aydencharles/onionHEN/releases/download/v0.0.11/OnionHEN.elf",
    "https://github.com/Gezine/BD-UN-JB/releases/download/1.1/bdj_unpatch_1340.elf",
    "https://github.com/ArkSama/PS5-Lapy-JB-Daemon/raw/main/lapy_jb_daemon.elf",
    "https://github.com/drakmor/nanoDNS/releases/download/0.2/nanodns-ps4.elf",
    "https://git.etawen.dev/soniciso/elf-arsenal/releases/download/v1.6.0/elf-arsenal.elf",
    "https://github.com/pegasus-ps5/pegasus-dl/releases/download/v1.7.0/pegasus_dl.elf",
    "https://github.com/notmaj0r/CheatRunner/releases/download/v0.14/CheatRunner.elf",
    "https://github.com/BestPig/BackPork/releases/download/0.1/ps5-backpork.elf",
    "https://github.com/ps4macedo/y2jb-p2jb/releases/download/1.0/P2JB_ASTRO_theme.elf",
    "https://github.com/ps4macedo/y2jb-p2jb/releases/download/1.0/TLOU_theme.elf",
    "https://github.com/ps4macedo/y2jb-p2jb/releases/download/1.0/P2JB_ZA_theme.elf",
)


def build_payload_source(url: str) -> PayloadSource:
    """Build one catalog entry using only the URL as source of truth."""
    normalized = normalize_payload_url(url)
    name, version = derive_payload_presentation(normalized)

    key_digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
    return PayloadSource(
        key=f"payload-{key_digest}",
        name=name,
        version=version,
        url=normalized,
    )


def build_payload_sources(urls: Iterable[str] = PAYLOAD_URLS) -> tuple[PayloadSource, ...]:
    sources = tuple(build_payload_source(url) for url in urls)
    keys = [source.key for source in sources]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate_payload_source")
    return sources


PAYLOAD_SOURCES = build_payload_sources()

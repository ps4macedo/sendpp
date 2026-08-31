from __future__ import annotations

from typing import Iterable

from app.models.pkg import PkgSource


PKG_INSTALLER_PORT = 9328
PKG_INSTALLER_MIN_VERSION = 14
PKG_UPLOAD_CHUNK_SIZE = 512 * 1024
PKG_INSTALL_STATUS_TIMEOUT_SECONDS = 15 * 60

REMOTE_PKG_CATALOG_SCHEMA_VERSION = 1
REMOTE_PKG_CATALOG_APP = "sendpp"
REMOTE_PKG_CATALOG_URL = "https://raw.githubusercontent.com/ps4macedo/sendpp/main/catalogs/pkg_catalog.json"

# Fonte fornecida pelo usuário. O aplicativo resolve releases mais novas em runtime.
KSTUFF_BASE_URL = "https://github.com/EchoStretch/kstuff-lite/releases/download/v1.10/kstuff.elf"
KSTUFF_ASSET_NAME = "kstuff.elf"


# -----------------------------------------------------------------------------
# CATÁLOGO DE PKGS
# -----------------------------------------------------------------------------
# PKG não tem nome seguro derivável em todos os links (ex.: pkg-zone/content-id).
# Por isso cada entrada tem chave estável, label explícito e URL.
# A lista online usa o mesmo contrato em pkg_catalog.json.
# -----------------------------------------------------------------------------
PKG_CATALOG_ENTRIES = (
    {
        "key": "ps5-xplorer",
        "label": "PS5-Xplorer 1.05",
        "url": "https://pkg-zone.com/download/ps5/LAPY20011/1.05",
    },
    {
        "key": "avatar-changer",
        "label": "Avatar Changer 1.00",
        "url": "https://pkg-zone.com/download/ps5/LAPY20016/1.00",
    },
    {
        "key": "ps5-temperature",
        "label": "PS5 Temperature 1.00",
        "url": "https://pkg-zone.com/download/ps5/LAPY20012/1.00",
    },
    {
        "key": "fpkg-i",
        "label": "FPKGi",
        "url": "https://pkg-zone.com/download/ps5/PKGI13337/latest",
    },
    {
        "key": "hbl",
        "label": "HBL v0.30",
        "url": "https://github.com/ps5-payload-dev/websrv/releases/download/v0.30/IV9999-FAKE00000_00-HOMEBREWLOADER01.pkg",
    },
    {
        "key": "youtube-us",
        "label": "YouTube (US) 1.03",
        "url": "https://pkg-zone.com/download/ps5/PPSA01650/1.03",
    },
    {
        "key": "netflix-eu",
        "label": "Netflix (EU)",
        "url": "https://pkg-zone.com/download/ps5/PPSA01615/6.00",
    },
)


def build_pkg_source(record: dict[str, str]) -> PkgSource:
    key = str(record.get("key", "") or "").strip()
    label = str(record.get("label", "") or "").strip()
    url = str(record.get("url", "") or "").strip()
    if not key or not label or not url:
        raise ValueError("pkg_source_invalid")
    return PkgSource(key, label, url)


def build_pkg_sources(entries: Iterable[dict[str, str]] = PKG_CATALOG_ENTRIES) -> tuple[PkgSource, ...]:
    sources = tuple(build_pkg_source(record) for record in entries)
    keys = [source.key.lower() for source in sources]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate_pkg_source")
    urls = [source.url.lower() for source in sources]
    if len(urls) != len(set(urls)):
        raise ValueError("duplicate_pkg_source_url")
    return sources


PKG_SOURCES = build_pkg_sources()

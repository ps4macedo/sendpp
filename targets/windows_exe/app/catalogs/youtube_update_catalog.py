import hashlib
import re
from pathlib import PurePosixPath
from typing import Iterable
from urllib.parse import unquote, urlparse

from app.models.youtube_update import (
    YOUTUBE_UPDATE_ALLOWED_EXTENSIONS,
    YOUTUBE_UPDATE_TARGET_DIR,
    YOUTUBE_UPDATE_TARGET_NAME,
    YouTubeUpdateSource,
)
from app.services.payload.payload_url_presentation import (
    derive_payload_presentation,
    normalize_payload_url,
)


REMOTE_YOUTUBE_UPDATE_CATALOG_SCHEMA_VERSION = 1
REMOTE_YOUTUBE_UPDATE_CATALOG_APP = "sendpp"
REMOTE_YOUTUBE_UPDATE_CATALOG_URL = "https://raw.githubusercontent.com/ps4macedo/sendpp/main/catalogs/youtube_update_catalog.json"

_RELEASE_PATH_RE = re.compile(
    r"/releases/download/(?P<tag>[^/]+)/(?P<asset>[^/?#]+)$",
    re.IGNORECASE,
)


# -----------------------------------------------------------------------------
# CATÁLOGO DE UPDATES DO YOUTUBE
# -----------------------------------------------------------------------------
# Esses itens NÃO são payloads TCP. O app baixa o .zip/.dat, prepara
# download0.dat e envia via FTPsrv para /user/download/PPSA01650/download0.dat.
# Para adicionar outro update, adicione SOMENTE a URL aqui ou no JSON online.
# -----------------------------------------------------------------------------
YOUTUBE_UPDATE_URLS = (
    "https://github.com/ps4macedo/y2jb-p2jb/releases/download/1.0/Y2JB_P2JB_AUTO_PSM.zip",
    "https://github.com/Gezine/Y2JB/releases/download/1.6/Y2JB_download0_1.6.zip",
    "https://github.com/itsPLK/ps5-y2jb-autoloader/releases/download/v0.9.1-36381e4/download0.dat",
)


def normalize_youtube_update_url(url: str) -> str:
    normalized = normalize_payload_url(url)
    filename = unquote(PurePosixPath(urlparse(normalized).path).name).strip().lower()
    if not filename.endswith(YOUTUBE_UPDATE_ALLOWED_EXTENSIONS):
        raise ValueError("youtube_update_url_extension_invalid")
    return normalized


def derive_youtube_update_presentation(url: str) -> tuple[str, str]:
    normalized = normalize_youtube_update_url(url)
    name, version = derive_payload_presentation(normalized)
    if version:
        return name, version

    release_match = _RELEASE_PATH_RE.search(unquote(urlparse(normalized).path or ""))
    release_tag = unquote(release_match.group("tag")).strip() if release_match else ""
    return name, release_tag


def build_youtube_update_source(url: str) -> YouTubeUpdateSource:
    normalized = normalize_youtube_update_url(url)
    name, version = derive_youtube_update_presentation(normalized)
    key_digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
    return YouTubeUpdateSource(
        key=f"youtube-update-{key_digest}",
        name=name,
        version=version,
        url=normalized,
        remote_dir=YOUTUBE_UPDATE_TARGET_DIR,
        remote_name=YOUTUBE_UPDATE_TARGET_NAME,
    )


def build_youtube_update_sources(urls: Iterable[str] = YOUTUBE_UPDATE_URLS) -> tuple[YouTubeUpdateSource, ...]:
    sources = tuple(build_youtube_update_source(url) for url in urls)
    keys = [source.key for source in sources]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate_youtube_update_source")
    return sources


YOUTUBE_UPDATE_SOURCES = build_youtube_update_sources()

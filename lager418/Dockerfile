ARG BUILD_FROM
ARG API_VERSION
ARG WEB_VERSION
# Overridable so the add-on can be built against locally-tagged artifacts:
# a ghcr.io/ prefix always round-trips to the registry, even when the image
# is already in the local store.
ARG API_IMAGE=ghcr.io/layer418/lager418-api
ARG WEB_IMAGE=ghcr.io/layer418/lager418-web

# The app repos' own release images (published by their bump prod CI on a v*
# tag) — this add-on only lifts /app out of them, it never runs them.
# --platform=$BUILDPLATFORM because the payload is pure JS — no native modules
# in either tree today, so one amd64 build serves every target arch.
# ponytail: add a native dep and this must become a real multi-arch pull.
FROM --platform=$BUILDPLATFORM ${API_IMAGE}:${API_VERSION} AS api
FROM --platform=$BUILDPLATFORM ${WEB_IMAGE}:${WEB_VERSION} AS web

FROM ${BUILD_FROM}

# ponytail: postgres major is pinned on purpose — an unpinned bump silently
# orphans /data/pg. Changing it needs a pg_upgrade step here.
# cups-client = lp/lpstat/lpoptions. The label printer lives on another host's
# CUPS (there is none in this container); CUPS_SERVER points the CLI at it.
RUN apk add --no-cache nodejs postgresql17 postgresql17-client python3 cups-client

# Bundled SearXNG, so the research agent needs no second add-on. Pinned to a
# commit: upstream publishes no release tags, and an unpinned clone would make
# every rebuild a different app. Every dep ships a musl wheel for both arches,
# so --only-binary keeps a compiler out of this image — drop the flag and the
# aarch64 build starts compiling lxml under qemu. The freeze step writes
# searx/version_frozen.py — without it searx shells out to git on every import
# and crashes in an image that has neither git nor a .git directory.
ARG SEARXNG_REF=2a6fc07be3760543c7b6d1d1bfe62f5765d5d9d6
RUN apk add --no-cache --virtual .searxng-build git py3-pip \
    && git clone https://github.com/searxng/searxng.git /opt/searxng \
    && git -C /opt/searxng checkout --detach "${SEARXNG_REF}" \
    && python3 -m venv /opt/searxng/venv \
    && /opt/searxng/venv/bin/pip install --no-cache-dir --only-binary :all: \
        -r /opt/searxng/requirements.txt \
    && (cd /opt/searxng && ./venv/bin/python -m searx.version freeze) \
    && rm -rf /opt/searxng/.git \
    && apk del .searxng-build

COPY --from=api /app /opt/api
COPY --from=web /app/.output /opt/web/.output
COPY rootfs /

LABEL io.hass.type="addon"

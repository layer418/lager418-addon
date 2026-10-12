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
RUN apk add --no-cache nodejs postgresql17 postgresql17-client

COPY --from=api /app /opt/api
COPY --from=web /app/.output /opt/web/.output
COPY rootfs /

LABEL io.hass.type="addon"

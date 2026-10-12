# LAGER418 — Home Assistant add-on repository

Runs the LAGER418 workshop inventory (NestJS API + Nuxt SPA + Postgres) as a
single Home Assistant add-on, behind ingress.

## Install

Settings → Add-ons → Add-on Store → ⋮ → Repositories → add:

```
https://github.com/layer418/lager418-addon
```

Then install **LAGER418** from the store and open it from the sidebar.

## Layout

```
repository.yaml            store listing
lager418/                  the add-on
  config.yaml              manifest (version here == published image tag)
  build.yaml               base image per arch + pinned API/WEB versions
  Dockerfile               assembles the two artifact images onto the HA base
  rootfs/                  s6 services: postgres → api → web
```

No application source lives here. Both app repos already publish
`ghcr.io/layer418/lager418-{api,web}:v<tag>` from their bump prod CI on a `v*`
tag; this Dockerfile just `COPY --from`s `/app` out of those images.

## Release

1. Tag `lager418-api` and `lager418-web` → their prod CI pushes
   `ghcr.io/layer418/lager418-{api,web}:v<version>`.
2. Bump `API_VERSION` / `WEB_VERSION` in `lager418/build.yaml` and `version:`
   in `lager418/config.yaml`, add a CHANGELOG entry.
3. Tag this repo `v<version>` → CI builds both arches and pushes
   `ghcr.io/layer418/lager418-{arch}:<version>`.

`version:` in `config.yaml` **must** equal the pushed image tag — that is the
entire update mechanism Supervisor uses.

## Developing

Day-to-day work happens in the app repos (`docker compose up` / `nuxt dev`)
against Keycloak + MinIO — `AUTH_MODE` and `STORAGE_DRIVER` default to that,
so the add-on's ingress/local-disk paths never get in the way.
To test the add-on itself, copy `lager418/` into `/addons/` on a real HA box
(SSH or Samba add-on) — it shows up under "Local add-ons" and Supervisor
builds it on the device:

```sh
ha addons rebuild local_lager418
ha addons logs local_lager418 -f
```

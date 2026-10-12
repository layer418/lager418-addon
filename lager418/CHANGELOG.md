# Changelog

## 0.1.1

- Create `/run/postgresql` on every boot — postgres FATAL'd in a restart loop
  without it.
- Consume the app repos' own release images instead of purpose-built artifact
  images.

## 0.1.0

- First packaging of LAGER418 as a Home Assistant add-on: API, SPA and
  Postgres in one container, behind ingress.

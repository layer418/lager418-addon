# Changelog

## 0.1.4

- Teile lassen sich ohne Foto anlegen — der Assistent startet jetzt auch
  ohne Kamera.
- Kein vorausgefüllter Lagerort mehr, der auf einer frischen Instanz gar
  nicht existiert (web v0.4.5).

## 0.1.3

- HA sensors: six per workshop plus an activity event entity, over MQTT
  discovery. Needs an MQTT broker; without one nothing changes.
- Fix a provisioning race that threw duplicate-key errors on the first page
  load, and return a readable 400 instead of a 500 when a part references a
  box that does not exist (api v0.1.4).

## 0.1.2

- Fix the blank page: the SPA shell's absolute `/_nuxt/` asset URLs 404'd
  behind the ingress path prefix (web v0.4.4).

## 0.1.1

- Create `/run/postgresql` on every boot — postgres FATAL'd in a restart loop
  without it.
- Consume the app repos' own release images instead of purpose-built artifact
  images.

## 0.1.0

- First packaging of LAGER418 as a Home Assistant add-on: API, SPA and
  Postgres in one container, behind ingress.

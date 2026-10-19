# Changelog

## 0.1.71

- App-Update: api v0.1.24, web v0.4.52.

## 0.1.70

- App-Update: api v0.1.23, web v0.4.52.

## 0.1.69

- App-Update: api v0.1.23, web v0.4.51.

## 0.1.68

- App-Update: api v0.1.22, web v0.4.51.

## 0.1.67

- App-Update: api v0.1.22, web v0.4.50.

## 0.1.66

- App-Update: api v0.1.22, web v0.4.49.

## 0.1.65

- App-Update: api v0.1.20, web v0.4.49.

## 0.1.64

- App-Update: api v0.1.19, web v0.4.49.

## 0.1.63

- App-Update: api v0.1.18, web v0.4.49.

## 0.1.62

- `searxng_url` und `research_base_url` stehen wieder in der Optionsliste.
  Seit 0.1.61 hatten sie keine Vorgabe mehr und die HA-Oberfläche versteckte
  sie hinter *Nicht verwendete optionale Konfigurationsoptionen einblenden*.
  Sie sind jetzt `str?` mit leerer Vorgabe — leer heißt weiterhin
  „mitgelieferte SearXNG“ bzw. „Recherche aus“.

## 0.1.61

- Add-on startet wieder: die leeren Vorgaben für `searxng_url` und
  `research_base_url` ließen die Optionsprüfung mit *expected a URL*
  scheitern. URL-Optionen haben jetzt gar keine Vorgabe — leer heißt
  weggelassen.

## 0.1.60

- SearXNG ist jetzt im Add-on enthalten und vorkonfiguriert (inklusive
  JSON-Format). Für die Bauteil-Recherche genügen damit die Modell-Optionen;
  ein zweites Add-on und `searxng_url` braucht es nicht mehr.
- `searxng_url` bleibt als Übersteuerung: gesetzt, benutzt das Add-on die
  eigene Instanz und startet die mitgelieferte nicht.
- Die Einstellungen der mitgelieferten Instanz liegen unter
  `/data/searxng/settings.yml` und überleben Updates.

## 0.1.59

- App-Update: api v0.1.17, web v0.4.49.

## 0.1.58

- App-Update: api v0.1.17, web v0.4.48.

## 0.1.57

- App-Update: api v0.1.16, web v0.4.48.

## 0.1.56

- Bauteil-Recherche: neue Optionen `searxng_url`, `research_base_url`,
  `research_api_key`, `research_model`. Ohne sie bleibt der Knopf verborgen.

## 0.1.55

- App-Update: api v0.1.16, web v0.4.47.

## 0.1.54

- App-Update: api v0.1.16, web v0.4.46.

## 0.1.53

- App-Update: api v0.1.16, web v0.4.45.

## 0.1.52

- App-Update: api v0.1.16, web v0.4.44.

## 0.1.51

- App-Update: api v0.1.15, web v0.4.44.

## 0.1.50

- App-Update: api v0.1.15, web v0.4.42.

## 0.1.49

- App-Update: api v0.1.13, web v0.4.42.

## 0.1.48

- App-Update: api v0.1.13, web v0.4.41.

## 0.1.47

- App-Update: api v0.1.13, web v0.4.40.

## 0.1.46

- App-Update: api v0.1.13, web v0.4.39.

## 0.1.45

- App-Update: api v0.1.13, web v0.4.38.

## 0.1.44

- App-Update: api v0.1.13, web v0.4.37.

## 0.1.43

- App-Update: api v0.1.13, web v0.4.36.

## 0.1.42

- App-Update: api v0.1.13, web v0.4.35.

## 0.1.41

- App-Update: api v0.1.13, web v0.4.34.

## 0.1.40

- App-Update: api v0.1.13, web v0.4.33.

## 0.1.39

- App-Update: api v0.1.13, web v0.4.32.

## 0.1.38

- App-Update: api v0.1.12, web v0.4.32.

## 0.1.37

- App-Update: api v0.1.12, web v0.4.31.

## 0.1.36

- App-Update: api v0.1.12, web v0.4.30.

## 0.1.35

- App-Update: api v0.1.12, web v0.4.29.

## 0.1.34

- App-Update: api v0.1.12, web v0.4.28.

## 0.1.33

- App-Update: api v0.1.12, web v0.4.27.

## 0.1.32

- App-Update: api v0.1.11, web v0.4.27.

## 0.1.31

- App-Update: api v0.1.11, web v0.4.26.

## 0.1.30

- App-Update: api v0.1.10, web v0.4.26.

## 0.1.29

- App-Update: api v0.1.10, web v0.4.25.

## 0.1.28

- App-Update: api v0.1.10, web v0.4.24.

## 0.1.27

- App-Update: api v0.1.10, web v0.4.23.

## 0.1.26

- App-Update: api v0.1.9, web v0.4.23.

## 0.1.25

- App-Update: api v0.1.9, web v0.4.22.

## 0.1.24

- App-Update: api v0.1.8, web v0.4.22.

## 0.1.23

- App-Update: api v0.1.8, web v0.4.21.

## 0.1.22

- App-Update: api v0.1.8, web v0.4.20.

## 0.1.21

- App-Update: api v0.1.8, web v0.4.19.

## 0.1.20

- App-Update: api v0.1.7, web v0.4.19.

## 0.1.19

- App-Update: api v0.1.7, web v0.4.13.

## 0.1.18

- App-Update: api v0.1.7, web v0.4.18.

## 0.1.17

- App-Update: api v0.1.7, web v0.4.17.

## 0.1.16

- App-Update: api v0.1.7, web v0.4.16.

## 0.1.15

- App-Update: api v0.1.7, web v0.4.15.

## 0.1.14

- App-Update: api v0.1.7, web v0.4.14.

## 0.1.13

- App-Update: api v0.1.6, web v0.4.14.

## 0.1.12

- App-Update: api v0.1.6, web v0.4.12.

## 0.1.11

- App-Update: api v0.1.6, web v0.4.11.

## 0.1.10

- App-Update: api v0.1.6, web v0.4.10.

## 0.1.9

- App-Update: api v0.1.6, web v0.4.9.

## 0.1.8

- App-Update: api v0.1.6, web v0.4.7. (0.1.7 wurde nie als Image
  veröffentlicht — die Release-Pipeline baute den Stand vor dem Bump.)

## 0.1.6

- Das Foto aus dem Anlege-Assistenten wird jetzt gespeichert und am
  Bauteil angezeigt — vorher ging es nach der KI-Erkennung verloren und
  die Detailseite zeigte nur einen Platzhalter (api v0.1.5, web v0.4.6).

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

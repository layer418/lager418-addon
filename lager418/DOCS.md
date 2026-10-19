# LAGER418

Workshop inventory: parts, boxes, shelves, projects, lending.

## Installation

Install the add-on and press **Start**. The first start initialises a Postgres
cluster in the add-on's `/data` and applies migrations — give it a minute.
Then open **Lager** from the sidebar.

## Configuration

| Option | Meaning |
| --- | --- |
| `anthropic_key` | API key for photo classification during ingest. Leave empty to disable the AI step — everything else works without it. |
| `anthropic_vision_model` | Vision model used for that step. Empty = the app default. |
| `jev_api_key` | TypeSafe/Jev key. Empty hides the dynamic-insert refine step in the UI. |
| `federation_enabled` | Expose `/api/federation/*` so other LAGER418 hosts can browse shared parts and run transfers. Off by default. |
| `federation_base_url` | The URL peers reach this instance on. Required when federation is enabled. |
| `federation_allow_private` | Accept peer URLs on loopback/LAN. Needed for LAN-only pairing, never for a publicly exposed instance. |
| `searxng_url` | Nur nötig, wenn du eine eigene SearXNG-Instanz benutzen willst. Leer = die mitgelieferte auf 127.0.0.1:8888. |
| `research_base_url` | OpenAI-compatible chat endpoint for the research agent. Empty hides the Recherchieren button. |
| `research_api_key` | Key for that endpoint. Leer lassen für ein lokales Modell ohne Schlüssel (Ollama, vLLM). |
| `research_model` | Model id to use, e.g. `claude-sonnet-5-5`, `gpt-4o-mini` oder `qwen2.5:14b`. |
| `research_max_tokens` | Token-Budget pro Recherche-Lauf. `0` = kein Limit. |
| `cups_server` | Netzwerk-CUPS mit dem Etikettendrucker, z.B. `192.168.1.20` oder `192.168.1.20:631`. Leer = kein Direktdruck, Etiketten gehen über den Browser-Druckdialog. |
| `log_level` | Add-on log verbosity. |

## Bauteil-Recherche

Der Knopf **Recherchieren** auf einer Bauteilseite sucht im Web nach Foto,
Datenblatt, Hersteller, Herstellernummer und Preis und schlägt die Funde zur
Übernahme vor. Übernommen wird nur, was angehakt wird; jeder Lauf bleibt als
Protokoll am Bauteil stehen.

Dafür braucht er ein Sprachmodell — die Suchmaschine bringt das Add-on mit.

**Die Suchmaschine.** Eine SearXNG-Instanz läuft im Add-on, erreichbar nur
containerintern auf `127.0.0.1:8888`, mit eingeschaltetem JSON-Format. Es ist
nichts einzurichten. Ihre Einstellungen stehen in `/data/searxng/settings.yml`;
die Datei wird beim ersten Start angelegt (mit eigenem `secret_key`) und bei
Updates nicht angefasst — dort lassen sich Engines ab- und zuschalten.

Du hast schon eine SearXNG-Instanz? Trage sie unter `searxng_url` ein, dann
benutzt das Add-on die und startet die eigene gar nicht erst. Zwei Stolpersteine
dabei: die Adresse eines anderen Add-ons enthält einen vom Supervisor
vergebenen Präfix (`ha addons info <slug>` zeigt sie unter `hostname`, sie sieht
aus wie `http://<präfix>-searxng:8080`), und deine Instanz muss `json` in
`search.formats` stehen haben — sonst bricht jeder Lauf mit einem Suchfehler ab.

**Das Sprachmodell.** `research_base_url` zeigt auf einen beliebigen
OpenAI-kompatiblen Endpunkt — OpenAI, OpenRouter, Groq, Mistral, Together,
Anthropic (`https://api.anthropic.com/v1`), oder ein lokales Ollama bzw. vLLM.
Dazu `research_api_key` und `research_model`. Das Modell muss Tool-Calling
beherrschen; sehr kleine lokale Modelle tun sich damit schwer.

**Was ein Lauf kosten darf.** `research_max_tokens` begrenzt, wie viele Token
ein einzelner Lauf verbrauchen darf — gezählt über alle Modellaufrufe des Laufs
hinweg, also so, wie der Anbieter abrechnet. Ist das Budget aufgebraucht, nimmt
der Agent die Werkzeuge weg und fordert die Antwort an: der Lauf endet mit einem
dünneren Vorschlag statt mit gar keinem. Dieser Abschlussaufruf wird noch
abgerechnet, die tatsächliche Obergrenze ist also Budget plus ein Aufruf. `0`
heißt kein Limit. Im Protokoll steht bei gesetztem Budget `N/BUDGET Token`.

Fehlt `research_base_url` oder `research_model`, erscheint der Knopf gar nicht
erst; das Add-on-Log nennt dann, welche Option fehlt.

Hinweis zur Sicherheit: Das Modell wählt selbst aus, welche Seiten gelesen
werden. Adressen im eigenen Netz werden dabei grundsätzlich abgelehnt —
`searxng_url` ist davon ausgenommen, weil es aus der Konfiguration stammt und
nicht vom Modell.

## Users

There is no separate login. Home Assistant authenticates you, and the add-on
takes your HA user as the LAGER418 user — the first one to open it gets an
org created and becomes its owner.

## Data

Everything lives in the add-on's `/data`: the Postgres cluster in `/data/pg`,
uploaded photos in `/data/photos`. Both are included in Home Assistant
backups and both are **deleted when the add-on is uninstalled**. Take a
backup before uninstalling.

## Sensors and automations

If an MQTT broker is installed (the Mosquitto add-on), LAGER418 registers
itself through MQTT discovery — no YAML, no restart. You get one device per
workshop with six sensors:

| Sensor | What it is |
|---|---|
| Teile | number of part records |
| Bestand | sum of all quantities |
| Lagerwert | stock value in EUR |
| Nachbestellen | parts below their minimum quantity |
| Verliehen | tools currently lent out |
| Aktive Projekte | projects in status `active` |

Plus an **Aktivität** event entity that fires on every change
(`parts.created`, `parts.movement`, `boxes.parts_moved`, …) with the
changed record as attributes — that is the one to trigger automations off:

```yaml
automation:
  - triggers:
      - trigger: state
        entity_id: sensor.lager418_low_stock
    conditions:
      - condition: numeric_state
        entity_id: sensor.lager418_low_stock
        above: 0
    actions:
      - action: notify.persistent_notification
        data:
          message: "{{ states('sensor.lager418_low_stock') }} Teile nachbestellen"
```

Without a broker the add-on starts and runs exactly as before, it just
publishes nothing.

## Lending between workshops

Connecting to another LAGER418 instance needs that instance to be reachable
from this one — the Tailscale add-on on both ends is the least painful route.

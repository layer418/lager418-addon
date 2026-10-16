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
| `searxng_url` | SearXNG instance used by the research agent. Empty hides the Recherchieren button. |
| `research_base_url` | OpenAI-compatible chat endpoint for the research agent. Empty hides the button. |
| `research_api_key` | Key for that endpoint. |
| `research_model` | Model id to use, e.g. `gpt-4o-mini` or `qwen2.5:14b`. |
| `log_level` | Add-on log verbosity. |

## Bauteil-Recherche

Der Knopf **Recherchieren** auf einer Bauteilseite sucht im Web nach Foto,
Datenblatt, Hersteller, Herstellernummer und Preis und schlägt die Funde zur
Übernahme vor. Übernommen wird nur, was angehakt wird; jeder Lauf bleibt als
Protokoll am Bauteil stehen.

Dafür braucht er zwei Dinge:

**1. Eine Suchmaschine.** Installiere ein SearXNG-Add-on und trage seine Adresse
unter `searxng_url` ein. Zwei Stolpersteine:

- *Die Adresse.* Add-ons erreichen einander unter einem Hostnamen, den der
  Supervisor vergibt — er enthält einen Präfix, der vom Repository abhängt, und
  ist deshalb bei jeder Installation anders. Den richtigen Wert zeigt
  `ha addons info <slug>` unter `hostname`, oder die Info-Seite des Add-ons.
  Er sieht aus wie `http://<präfix>-searxng:8080`.
- *Das JSON-Format.* SearXNG liefert standardmäßig **nur HTML**. In
  `addon_configs/.../settings.yml` muss `json` in der Formatliste stehen:

  ```yaml
  search:
    formats:
      - html
      - json
  ```

  Fehlt es, kommt auf jede Suche eine HTML-Seite zurück und jeder Lauf bricht
  mit einem Suchfehler im Protokoll ab.

**2. Ein Sprachmodell.** `research_base_url` zeigt auf einen beliebigen
OpenAI-kompatiblen Endpunkt — OpenAI, OpenRouter, Groq, Mistral, Together, oder
ein lokales Ollama bzw. vLLM. Dazu `research_api_key` und `research_model`. Das
Modell muss Tool-Calling beherrschen; sehr kleine lokale Modelle tun sich damit
schwer.

Sind nicht alle vier Optionen gesetzt, erscheint der Knopf gar nicht erst.

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

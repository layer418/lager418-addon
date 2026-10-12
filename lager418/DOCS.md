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
| `log_level` | Add-on log verbosity. |

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

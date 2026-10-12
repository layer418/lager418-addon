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

## Lending between workshops

Connecting to another LAGER418 instance needs that instance to be reachable
from this one — the Tailscale add-on on both ends is the least painful route.

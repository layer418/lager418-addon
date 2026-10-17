"""Every default in config.yaml must survive Supervisor's option validation.

The trap this exists for: schema "url?" means the key may be *absent*, not that
it may be empty — a default of "" reaches vol.Url() and the add-on dies on
start with "expected a URL". Same for email/port/match.

    pip install voluptuous pyyaml && python tests/test_options.py
"""

import pathlib
import re
import sys

import voluptuous as vol
import yaml

CONFIG = pathlib.Path(__file__).resolve().parent.parent / "lager418" / "config.yaml"

# The subset of Supervisor's types this add-on uses, same validators it uses.
VALIDATORS = {
    "str": str,
    "password": str,
    "bool": vol.Boolean(),
    "int": vol.Coerce(int),
    "float": vol.Coerce(float),
    "email": vol.Email(),
    "url": vol.Url(),
    "port": vol.Coerce(int),
}


def validate(typ: str, value) -> None:
    if match := re.match(r"^list\((.*)\)\??$", typ):
        vol.In(match.group(1).split("|"))(str(value))
        return
    base = re.match(r"^[a-z]+", typ).group(0)
    if base not in VALIDATORS:
        raise AssertionError(f"test does not know type {typ!r} — teach it")
    VALIDATORS[base](value)


def main() -> int:
    config = yaml.safe_load(CONFIG.read_text())
    options, schema = config["options"], config["schema"]

    failures = []
    for key, value in options.items():
        if key not in schema:
            failures.append(f"{key}: default has no schema entry")
            continue
        try:
            validate(schema[key], value)
        except vol.Invalid as err:
            failures.append(f"{key}: default {value!r} fails {schema[key]!r} — {err}")

    # A default is only optional-by-absence if the schema says so.
    for key, typ in schema.items():
        if key not in options and not typ.endswith("?"):
            failures.append(f"{key}: required by schema but has no default")

    for line in failures:
        print(f"FAIL {line}")
    print(f"{len(options)} defaults checked, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

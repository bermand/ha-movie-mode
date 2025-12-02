"""Blueprint validation MVP for Movie Mode.

This script performs a lightweight check of the movie-mode blueprint and
prepares a temporary Home Assistant configuration directory suitable for
running ``hass --script check_config``.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml
except ImportError as err:  # pragma: no cover - dependency guard
    sys.stderr.write("PyYAML is required to run this validator.\n")
    raise


DEFAULT_FIXTURES = {
    "media_player": "media_player.living_room",
    "movie_mode_helper": "input_boolean.movie_mode_active",
    "notify_target": "test_device",
    "controlled_entities": {"entity_id": ["light.movie_light", "switch.movie_switch"]},
    "movie_scene": "scene.movie_mode",
    "start_time": "21:00:00",
    "notify_title": "Movie Mode",
    "notify_message": "Turn on Movie Mode?",
    "trigger_on_state": ["playing"],
    "trigger_pause_state": ["paused"],
    "trigger_off_state": ["idle"],
    "app_cond": [],
}


def load_blueprint(path: Path) -> Dict[str, Any]:
    raw = yaml.safe_load(path.read_text())
    if not isinstance(raw, dict) or "blueprint" not in raw:
        raise ValueError("File does not contain a Home Assistant blueprint definition")
    return raw["blueprint"]


def validate_blueprint_structure(bp: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for required in ("name", "description", "domain", "input"):
        if required not in bp:
            issues.append(f"Missing required blueprint key: {required}")
    if bp.get("domain") != "automation":
        issues.append("Blueprint domain should be 'automation'.")
    inputs = bp.get("input", {})
    if not isinstance(inputs, dict) or not inputs:
        issues.append("Blueprint inputs are empty or invalid.")
    return issues


def merge_default_inputs(bp: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(DEFAULT_FIXTURES)
    for key, meta in bp.get("input", {}).items():
        if isinstance(meta, dict) and "default" in meta:
            merged.setdefault(key, meta["default"])
    return merged


def build_configuration(blueprint_filename: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "homeassistant": {
            "name": "Blueprint Validation",
            "latitude": 0,
            "longitude": 0,
            "elevation": 0,
            "unit_system": "metric",
            "time_zone": "UTC",
        },
        "input_boolean": {
            "movie_mode_active": {"name": "Movie Mode Active"},
            "movie_light_power": {"name": "Movie Light Power"},
            "movie_switch_power": {"name": "Movie Switch Power"},
        },
        "light": [
            {
                "platform": "template",
                "lights": {
                    "movie_light": {
                        "value_template": "{{ is_state('input_boolean.movie_light_power', 'on') }}",
                        "turn_on": {"service": "input_boolean.turn_on", "target": {"entity_id": "input_boolean.movie_light_power"}},
                        "turn_off": {"service": "input_boolean.turn_off", "target": {"entity_id": "input_boolean.movie_light_power"}},
                    }
                },
            }
        ],
        "switch": [
            {
                "platform": "template",
                "switches": {
                    "movie_switch": {
                        "value_template": "{{ is_state('input_boolean.movie_switch_power', 'on') }}",
                        "turn_on": {"service": "input_boolean.turn_on", "target": {"entity_id": "input_boolean.movie_switch_power"}},
                        "turn_off": {"service": "input_boolean.turn_off", "target": {"entity_id": "input_boolean.movie_switch_power"}},
                    }
                },
            }
        ],
        "scene": [
            {
                "name": "Movie Mode",
                "entities": {
                    "light.movie_light": "off",
                    "switch.movie_switch": "off",
                },
            },
            {
                "name": "Movie Mode Previous State",
                "entities": {
                    "input_boolean.movie_mode_active": "off",
                },
            },
        ],
        "notify": [
            {
                "name": "test_device",
                "platform": "file",
                "filename": "notify_test_device.log",
            }
        ],
        "media_player": [
            {"platform": "demo"},
        ],
        "automation": [
            {
                "use_blueprint": {
                    "path": f"local/{blueprint_filename}",
                    "input": inputs,
                }
            }
        ],
    }


def write_config_bundle(output_dir: Path, blueprint_path: Path, inputs: Dict[str, Any]) -> Tuple[Path, Path]:
    bp_dir = output_dir / "blueprints" / "automation" / "local"
    bp_dir.mkdir(parents=True, exist_ok=True)
    bp_dest = bp_dir / blueprint_path.name
    shutil.copy2(blueprint_path, bp_dest)

    config = build_configuration(blueprint_path.name, inputs)
    config_path = output_dir / "configuration.yaml"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False))
    return bp_dest, config_path


def run_check_config(config_dir: Path) -> Tuple[bool, str]:
    hass_path = shutil.which("hass")
    if not hass_path:
        return False, "Home Assistant (hass) CLI not found. Install Home Assistant to run check_config."

    process = subprocess.run(
        [hass_path, "--script", "check_config", "--config", str(config_dir)],
        check=False,
        capture_output=True,
        text=True,
    )
    output = process.stdout + process.stderr
    return process.returncode == 0, output


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Movie Mode blueprint and prepare a test config.")
    parser.add_argument("blueprint", type=Path, help="Path to the movie-mode blueprint YAML file")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".ha-validator"),
        help="Directory where the temporary Home Assistant config will be written",
    )
    parser.add_argument("--run-check-config", action="store_true", help="Run hass --script check_config if available")
    args = parser.parse_args()

    blueprint = load_blueprint(args.blueprint)
    issues = validate_blueprint_structure(blueprint)
    if issues:
        sys.stderr.write("\n".join(f"[schema] {issue}" for issue in issues) + "\n")
        sys.exit(1)

    merged_inputs = merge_default_inputs(blueprint)
    bp_dest, config_path = write_config_bundle(args.output, args.blueprint, merged_inputs)

    print(f"Blueprint copied to: {bp_dest}")
    print(f"Configuration written to: {config_path}")

    if args.run_check_config:
        success, message = run_check_config(args.output)
        status = "passed" if success else "failed"
        print(f"check_config {status}\n{message}")
    else:
        print("check_config not run (use --run-check-config to enable)")


if __name__ == "__main__":
    main()

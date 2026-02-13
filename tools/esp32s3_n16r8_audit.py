#!/usr/bin/env python3
"""Validate ESP32-S3 N16R8 CNC board integration and emit a concise audit log.

This script checks the key pin and feature definitions that are critical for the
custom CNC board profile. It is designed for quick local validation without
requiring PlatformIO.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def extract_define(file_path: Path, macro: str) -> str | None:
    """Return the macro value for a '#define <macro> <value>' entry.

    Slovensky: Funkcia vyhlada hodnotu makra v C/C++ hlavičke.
    Vracia None, ak makro nie je definované.
    """
    rx = re.compile(rf"^\s*#define\s+{re.escape(macro)}(?:\s+(.*?))?\s*$")
    for line in file_path.read_text(encoding="utf-8").splitlines():
        m = rx.match(line)
        if m:
            return (m.group(1) or '').strip()
    return None


def check_equals(file_path: Path, macro: str, expected: str, report: list[str]) -> bool:
    """Check that a macro equals an expected value and append report output."""
    value = extract_define(file_path, macro)
    ok = value == expected
    report.append(f"{'OK' if ok else 'FAIL'} {file_path.relative_to(REPO_ROOT)} :: {macro} = {value!r} (expected {expected!r})")
    return ok


def contains_text(file_path: Path, needle: str, report: list[str]) -> bool:
    """Check whether a file contains a specific text fragment."""
    found = needle in file_path.read_text(encoding="utf-8")
    report.append(f"{'OK' if found else 'FAIL'} {file_path.relative_to(REPO_ROOT)} contains: {needle}")
    return found


def run_audit() -> tuple[bool, list[str]]:
    """Run all checks for board registration, pin mapping, and core config."""
    report: list[str] = []
    ok = True

    pins = REPO_ROOT / "Marlin/src/pins/esp32/pins_ESP32S3_N16R8_CNC.h"
    boards = REPO_ROOT / "Marlin/src/core/boards.h"
    pins_router = REPO_ROOT / "Marlin/src/pins/pins.h"
    cfg = REPO_ROOT / "Marlin/Configuration.h"
    cfg_adv = REPO_ROOT / "Marlin/Configuration_adv.h"

    expected_pins = {
        "X_STEP_PIN": "4",
        "X_DIR_PIN": "5",
        "Y_STEP_PIN": "6",
        "Y_DIR_PIN": "7",
        "Y2_STEP_PIN": "12",
        "Y2_DIR_PIN": "13",
        "Z_STEP_PIN": "10",
        "Z_DIR_PIN": "11",
        "X_ENABLE_PIN": "8",
        "X_MIN_PIN": "15",
        "Y_MIN_PIN": "16",
        "Z_MIN_PIN": "17",
        "Y2_STOP_PIN": "18",
        "SPINDLE_LASER_ENA_PIN": "14",
        "SPINDLE_LASER_PWM_PIN": "1",
        "CASE_LIGHT_PIN": "21",
        "HARDWARE_SERIAL1_RX": "44",
        "HARDWARE_SERIAL1_TX": "43",
    }

    for macro, expected in expected_pins.items():
        ok &= check_equals(pins, macro, expected, report)

    ok &= contains_text(boards, "#define BOARD_ESP32S3_N16R8_CNC", report)
    ok &= contains_text(pins_router, "#elif MB(ESP32S3_N16R8_CNC)", report)

    config_expectations = {
        "MOTHERBOARD": "BOARD_ESP32S3_N16R8_CNC",
        "SERIAL_PORT": "1",
        "EXTRUDERS": "0",
        "TEMP_SENSOR_0": "0",
        "TEMP_SENSOR_BED": "0",
        "ENDSTOP_INTERRUPTS_FEATURE": "",
    }

    for macro, expected in config_expectations.items():
        if expected:
            ok &= check_equals(cfg, macro, expected, report)
        else:
            # boolean-style macro without value
            found = extract_define(cfg, macro) is not None
            report.append(f"{'OK' if found else 'FAIL'} {cfg.relative_to(REPO_ROOT)} :: {macro} defined")
            ok &= found

    ok &= contains_text(cfg_adv, "#define Y_DUAL_ENDSTOPS", report)
    ok &= contains_text(cfg_adv, "#define LASER_FEATURE", report)

    return ok, report


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Audit ESP32-S3 N16R8 CNC Marlin integration")
    parser.add_argument("--log-file", default="log.txt", help="Path to audit log file (default: log.txt)")
    args = parser.parse_args()

    ok, report = run_audit()

    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"ESP32-S3 N16R8 CNC Audit @ {stamp}", "=" * 72, *report, "", f"RESULT: {'PASS' if ok else 'FAIL'}", ""]

    log_path = REPO_ROOT / args.log_file
    log_path.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

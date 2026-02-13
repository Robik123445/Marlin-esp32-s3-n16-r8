# ESP32-S3 N16R8 CNC – Compatibility Notes

Short answer: **yes, there can still be compatibility issues** even with correct pin mapping.
This file tracks the realistic risks and how to validate them quickly.

## 1) PWM on GPIO1 (laser)

- `GPIO1` works as LEDC PWM, but on some ESP32-S3 board variants it may have boot/console side-effects.
- If you see unstable laser output during boot or reconnect events, test an alternate PWM-capable GPIO.

**Check**
- Scope on GPIO1 while sending `M3 S0/S64/S128/S255`.
- Ensure duty transitions are monotonic and stable.

## 2) UART mapping (RX44 / TX43)

- Mapping is valid via GPIO matrix, but host adapters / cable quality can still cause stream drops.

**Check**
- Long dry-run streaming (15–30 min).
- Watch for `Resend`, checksum bursts, random pauses.

## 3) Dual-Y endstop squaring

- Firmware side is enabled (`Y_DUAL_ENDSTOPS`), but mechanical asymmetry and endstop repeatability still matter.

**Check**
- Repeated `G28 Y` (10x+), measure gantry skew.
- Tune via `M666 Y<offset>` and store with `M500`.

## 4) ESP32 package/toolchain drift

- ESP32 Arduino package versions can change timer/interrupt behavior.
- Using a dedicated board profile (`marlin_ESP32S3_N16R8`) reduces mismatch risk.

**Check**
- Keep the environment locked (`espressif32@~6.7.0`) unless intentionally upgrading.
- Re-run smoke + audit after any package bump.

## 5) Motion jitter under load

- Even with valid pins, CNC quality depends on pulse timing under planner + serial load.

**Check**
- Long diagonal and arc jobs with laser enabled.
- Confirm no audible stutter / no lost steps.

## Fast validation commands

```gcode
M115
M119
G28
M3 S0
M3 S128
M3 S255
M5
```

And locally:

```bash
python3 tools/esp32s3_n16r8_audit.py
```

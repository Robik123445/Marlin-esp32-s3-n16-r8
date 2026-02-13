# ESP32-S3 N16R8 CNC – Next Steps (without PlatformIO)

This checklist is focused on your current state: board + pins are integrated.
Now the goal is to harden behavior for CNC (laser + milling), verify motion stability,
and finalize operational presets.

## 1) Electrical / pin bring-up (hardware-first)

1. Flash firmware with current board profile.
2. Run `M43` and verify pin visibility.
3. Run `M119` and manually trigger endstops:
   - X min = GPIO15
   - Y min = GPIO16
   - Z min = GPIO17
   - Y2 min = GPIO18
4. Verify step/dir outputs with logic probe:
   - X: STEP4, DIR5
   - Y: STEP6, DIR7
   - Y2: STEP12, DIR13
   - Z: STEP10, DIR11
5. Verify shared enable GPIO8 (all axes disable on `M18`).

## 2) Dual-Y gantry alignment (critical)

Current config enables:
- `Y2_DRIVER_TYPE`
- `Y_DUAL_ENDSTOPS`

Validation sequence:
- `M119` -> ensure both `y_min` and `y2_min` report correctly.
- `G28 Y` repeatedly (10x).
- Measure gantry skew after homing (left/right reference difference).
- If offset exists, tune with `M666 Y<offset>` and store via `M500`.

## 3) Laser / spindle output validation

Pins:
- Enable: GPIO14
- PWM: GPIO1 (LEDC)

Smoke test G-code:
- `M3 S0`
- `M3 S64`
- `M3 S128`
- `M3 S255`
- `M5`

Observe with scope:
- Frequency around configured value (`SPINDLE_LASER_FREQUENCY`)
- Duty linearity between S values

## 4) UART streaming stability (RX44 / TX43)

Current config uses `SERIAL_PORT 1` with remapped pins.

Recommended test:
- Send long G-code stream (15–30 min dry run)
- Watch for:
  - pauses
  - checksum errors
  - resend storms
  - watchdog resets

## 5) Motion and jitter hardening

Even if functional, do a step pulse quality pass:
- High feed straight lines and diagonals
- Arc interpolation stress (`G2/G3`)
- Confirm no audible stutter or lost steps

If needed next:
- Tune accel/jerk limits for CNC mass
- Optionally profile ISR load around stepper + endstop interrupts

## 6) Keep an audit trail

Use:
```bash
python3 tools/esp32s3_n16r8_audit.py
```

This writes `log.txt` with current pin/config checks and PASS/FAIL summary.

## 7) Suggested immediate next implementation tasks

- Add board-specific `*_adv.h` profile presets for laser vs spindle workflows.
- Add machine-safe defaults (`M203/M201/M204`) tuned for your mechanics.
- Add a minimal startup macro block (safe laser-off, coordinate mode, feed mode).
- Add a dedicated validation G-code suite (already started in `buildroot/test-gcode`).

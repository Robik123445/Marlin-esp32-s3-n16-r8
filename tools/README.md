# Tools

## `esp32s3_n16r8_audit.py`

Quick static audit for the custom ESP32-S3 N16R8 CNC integration.

### What it checks
- Board registration in `boards.h`
- Board routing in `pins.h`
- Pin values in `pins_ESP32S3_N16R8_CNC.h`
- Key CNC config macros in `Configuration.h` / `Configuration_adv.h`
- Presence of custom board profile `marlin_ESP32S3_N16R8` and env binding in `ini/esp32.ini`

### Usage
```bash
python3 tools/esp32s3_n16r8_audit.py
```

Optional custom log path:
```bash
python3 tools/esp32s3_n16r8_audit.py --log-file log.txt
```

### Output
- Console PASS/FAIL report
- `log.txt` audit artifact in repository root

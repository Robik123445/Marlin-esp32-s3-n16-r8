; ESP32-S3 N16R8 CNC smoke test
; Purpose: quick post-flash validation of endstops, motion, and laser PWM

M115
M119

; Home
G28

; Basic XY motion
G90
G0 X10 Y10 F3000
G0 X50 Y10
G0 X50 Y50
G0 X10 Y50
G0 X10 Y10

; Z motion
G0 Z5 F600
G0 Z1 F600

; Laser PWM test
M3 S0
G4 P500
M3 S64
G4 P500
M3 S128
G4 P500
M3 S255
G4 P500
M5

; End
M400
M114

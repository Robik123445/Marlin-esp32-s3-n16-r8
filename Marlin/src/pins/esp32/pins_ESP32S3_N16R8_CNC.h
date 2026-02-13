/**
 * Marlin 3D Printer Firmware
 * Copyright (c) 2024 MarlinFirmware [https://github.com/MarlinFirmware/Marlin]
 *
 * Based on Sprinter and grbl.
 * Copyright (c) 2011 Camiel Gubbels / Erik van der Zalm
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 */
#pragma once

/**
 * ESP32-S3 WROOM N16R8 CNC controller pin assignments.
 *
 * CNC-only oriented map with dual Y support (Y2 on dedicated driver),
 * spindle / laser enable and hardware PWM output, and remapped UART pins.
 */

#include "env_validate.h"

#if HOTENDS || E_STEPPERS
  #error "ESP32S3_N16R8_CNC is CNC-only. Set EXTRUDERS to 0."
#endif

#define BOARD_INFO_NAME "ESP32-S3 N16R8 CNC"

#ifndef DEFAULT_MACHINE_NAME
  #define DEFAULT_MACHINE_NAME BOARD_INFO_NAME
#endif

//
// Disable I2S stepper stream for this board.
// Native GPIO step/dir is used to keep pin ownership explicit.
//
#undef I2S_STEPPER_STREAM

//
// Primary UART remap for host communication
//
#ifndef HARDWARE_SERIAL1_RX
  #define HARDWARE_SERIAL1_RX                 44
#endif
#ifndef HARDWARE_SERIAL1_TX
  #define HARDWARE_SERIAL1_TX                 43
#endif

//
// Limit Switches
//
#define X_MIN_PIN                             15
#define Y_MIN_PIN                             16
#define Z_MIN_PIN                             17
#define Y2_STOP_PIN                           18

//
// Steppers
//
#define X_STEP_PIN                             4
#define X_DIR_PIN                              5
#define X_ENABLE_PIN                           8

#define Y_STEP_PIN                             6
#define Y_DIR_PIN                              7
#define Y_ENABLE_PIN                  X_ENABLE_PIN

#define Y2_STEP_PIN                           12
#define Y2_DIR_PIN                            13
#define Y2_ENABLE_PIN                 X_ENABLE_PIN

#define Z_STEP_PIN                            10
#define Z_DIR_PIN                             11
#define Z_ENABLE_PIN                  X_ENABLE_PIN

//
// CNC spindle / laser
//
#define SPINDLE_LASER_ENA_PIN                 14
#define SPINDLE_LASER_PWM_PIN                  1

//
// Auxiliary output
//
#define CASE_LIGHT_PIN                        21

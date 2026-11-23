# Power and Sensor Architecture

In this README, we will go into detail on the electrical design, circuit diagram, modules, and electronic choices behind our vehicle.

## Schematic

<p align="center">
  <img src="../assets/electronics/schematic.png" alt="Full Electrical Schematic Diagram" width="800"/>
  <br>
  Complete Electrical Schematic Diagram
</p>

## Perfboard Assembly

To keep wiring compact and prevent loose connections from track vibrations, we soldered a custom perfboard to distribute power from the 3S 18650 battery pack to our three buck converters, motor driver, and ESP32 shield with a clean common ground.

<table>
  <tr>
    <td align="center" width="33%">
      <img src="../assets/electronics/perfboard-top.jpg" alt="Perfboard Top View" width="260"/><br>
      Top View
    </td>
    <td align="center" width="33%">
      <img src="../assets/electronics/perfboard-bottom.jpg" alt="Perfboard Bottom View" width="260"/><br>
      Bottom View
    </td>
    <td align="center" width="33%">
      <img src="../assets/electronics/perfboard-robot.jpg" alt="Perfboard Installed in Robot" width="260"/><br>
      Installed in Robot (Isometric)
    </td>
  </tr>
</table>

### Assembly Process

### Challenges

## Subsystems

### 1. Computing

We divided the computing workload between the **Raspberry Pi 4** and the **ESP32**. The Raspberry Pi 4 handles high-level decision-making and camera processing, while the ESP32 manages real-time actuator control. Both boards communicate directly via a USB serial connection. By running the Arduino IDE directly on the Raspberry Pi, we can edit and upload firmware to the ESP32 on the robot without needing to disconnect it or plug it into an external laptop.

### 2. Power Regulation

We divided voltage regulation into three isolated buck converter modules:
- **Compute Rail:** Supplies 5.1 V to the Raspberry Pi 4, which in turn powers the ESP32 via USB and provides 3.3 V to the MPU-9250 IMU and ToF sensors.
- **Drivetrain Rail:** Steps down voltage to 9.0 V for the LEGO EV3 drive motor.
- **Steering Rail:** Supplies 5.5 V dedicated to the steering servo.

### 3. Power Regulation Modules

#### XL4015 DC-DC Buck Converter (x2)

We selected two **XL4015** step-down modules to independently power the **Raspberry Pi 4 (5.1 V)** and the **Hitec HS-485HB steering servo (5.5 V)**. Its 5 A current rating provides plenty of headroom to handle CPU/camera load spikes on the Pi and sudden stall currents on the steering servo without voltage dips, while its high switching efficiency keeps heat low on the compact chassis.

<p align="center">
  <img src="../assets/components/xl4015.jpg" alt="XL4015 DC-DC Buck Converter" width="260"/><br>
  XL4015 5 A Step-Down Converter
</p>

| Specification | Value |
| :--- | :--- |
| **Input Voltage** | 4 V – 38 V DC |
| **Output Voltage** | 1.25 V – 36 V DC (Adjustable) |
| **Max Output Current** | 5.0 A (4.0 A continuous without heatsink) |
| **Switching Frequency** | 180 kHz |
| **Efficiency** | Up to 96% |

---

#### LM2596 DC-DC Buck Converter

We chose the **LM2596** step-down module to regulate voltage from the 3S battery pack down to **9.0 V** for the **L298N motor driver and LEGO EV3 drive motor**. It is compact, reliable, and easily handles the nominal current draw of the drive motor while isolating motor switching noise from the compute and servo rails.

<p align="center">
  <img src="../assets/components/lm2596.jpg" alt="LM2596 DC-DC Buck Converter" width="260"/><br>
  LM2596 3 A Step-Down Converter
</p>

| Specification | Value |
| :--- | :--- |
| **Input Voltage** | 3.2 V – 40 V DC |
| **Output Voltage** | 1.25 V – 35 V DC (Adjustable) |
| **Max Output Current** | 3.0 A |
| **Switching Frequency** | 150 kHz |
| **Efficiency** | Up to 92% |
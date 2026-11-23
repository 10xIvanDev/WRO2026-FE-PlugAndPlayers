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
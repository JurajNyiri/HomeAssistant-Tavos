# tavosWaterOutage Home Assistant sensor
Processes water outages from Tavos and provides them inside Home Assistant

## Installation:
Copy file sensor.py to custom_components/tavosWaterOutage/sensor.py

## Usage:
Add to configuration.yaml:

```
sensor:
  - platform: tavosWaterOutage
    name: [Optional - name]
    monitored_conditions: [Optional, list of cities/streets to monitor]
        - Example1
        - Example2
```

- State of the entity becomes nonempty if there is upcoming water outage for one of your monitored cities or streets.
- Attributes of the entity list all the outages.

# Disclaimer

Project and/or author is in no way associated with Tavos and provides this code completely free, according to LICENSE file.
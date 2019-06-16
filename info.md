## Usage:
Add to configuration.yaml:

```
sensor:
  - platform: tavos_water_outage
    name: [Optional - name]
    monitored_conditions: [Optional, list of cities/streets to monitor]
        - Example1
        - Example2
```

- State of the entity becomes nonempty if there is upcoming water outage for one of your monitored cities or streets.
- Attributes of the entity list all the outages.

# Disclaimer

Project and/or author is in no way associated with Tavos and provides this code completely free, according to LICENSE file.
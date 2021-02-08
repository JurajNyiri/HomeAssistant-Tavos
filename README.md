# tavos_water_outage Home Assistant sensor

Processes water outages from Tavos and provides them inside Home Assistant

## Installation

Copy contents of custom_components/tavos_water_outage/ to custom_components/tavos_water_outage/ in your Home Assistant config folder.

## Installation using HACS

HACS is a community store for Home Assistant. You can install [HACS](https://github.com/custom-components/hacs) and then install Tavos Water Outage from the HACS store.

## Usage

Add monitored cities or streats via Integrations (search for Tavos) in Home Assistant UI.

To add multiple monitored cities or streets, add integration multiple times.

Sensor entities in format of sensor.tavos*water_outage*_city/street_ will be created.

- State of the entity becomes nonempty if there is upcoming water outage for that monitored city/street
- Attributes of the entity list all the current outages
- If there are no current outages, sensor will be completely empty and that is expected.

### Usage example

**Automation to notify as soon when there is an upcoming outage in monitored city / street and then every day at 5pm:**

```yaml
- id: "1551393505029"
  alias: Send Water Outage Alert
  trigger:
    - at: "17:00:00"
      platform: time
    - platform: template
      value_template: "{{ states('sensor.tavos_water_outage_city')|string != '' }}"
  condition:
    - condition: template
      value_template: "{{ states('sensor.tavos_water_outage_city')|string != '' }}"
  action:
    - data_template:
        message:
          "Water outage alert: {{ states('sensor.tavos_water_outage_city')|string
          }}"
      service: notify.facebook
```

# Disclaimer

Project and/or author is in no way associated with Tavos and provides this code completely free, according to LICENSE file.

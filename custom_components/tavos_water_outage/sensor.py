"""
Support for Tavos Water Outage
configuration.yaml
sensor:
  - platform: tavos_water_outage
"""

__version__ = "0.3.4"

import logging
import json
import voluptuous as vol
import re

from datetime import timedelta,datetime

from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.helpers.entity import Entity
from homeassistant.const import (CONF_NAME, CONF_MONITORED_CONDITIONS)
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

DEFAULT_NAME = "Tavos Water Outage"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_MONITORED_CONDITIONS, default=[]): vol.All(cv.ensure_list)
})

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_SCANS = timedelta(seconds=600) #10 minutes

def setup_platform(hass, config, add_devices, discovery_info=None):
    import tavosPy
    add_devices([TavosWaterOutage(config)])


class TavosWaterOutage(Entity):

    def __init__(self, config):
        import tavosPy
        self._state = ""
        self._all_outages = {}
        self._name = config.get(CONF_NAME)
        self._monitored_conditions = config.get(CONF_MONITORED_CONDITIONS)
        self.tavospy = tavosPy.TavosPy()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @Throttle(MIN_TIME_BETWEEN_SCANS)
    def update(self):
        self.manualUpdate()

    @property
    def device_state_attributes(self):
        return self._all_outages

    def manualUpdate(self):
        if(self.tavospy.update()):
            self._state = ""
            tavosData = self.tavospy.getData()
            self._all_outages = {}
            for waterOutage in tavosData:
                attribute = ""
                if(waterOutage['date']['start']):
                    attribute = attribute + waterOutage['date']['start'].strftime("%d.%m.%Y %H:%M")
                if(waterOutage['date']['end']):
                    attribute = attribute + " - " + waterOutage['date']['end'].strftime("%d.%m.%Y %H:%M")
                
                value = ""
                if(waterOutage['city'] != ""):
                    value = value + waterOutage['city']
                if(waterOutage['street'] != ""):
                    value = value + " (" + waterOutage['street'] + ")"
                if(waterOutage['typeOfDefect'] != ""):
                    value = value + " - " + waterOutage['typeOfDefect']
                if(waterOutage['notes'] != ""):
                    value = value + " (" + waterOutage['notes'] + ")"
                if(attribute != "" and value != ""):
                    self._all_outages[attribute] = value


                for city in self._monitored_conditions:

                    isMonitored = (city in waterOutage['city'] or city in waterOutage['street'])
                    isInFuture = ((waterOutage['date']['start'] != False and datetime.now() < waterOutage['date']['start']) or (waterOutage['date']['end'] != False and datetime.now() < waterOutage['date']['end']))

                    if(isMonitored and isInFuture):
                        if(self._state != ""):
                            self._state = self._state + "\r\n" + attribute + ": " + value
                        else:
                            self._state = attribute + ": " + value
        else:
            _LOGGER.warn("Update for tavosWaterOutage failed.")

from typing import Callable
from datetime import datetime
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from .const import MONITORED_STRING, DOMAIN, _LOGGER


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable
):
    try:
        return async_add_entities(
            [TavosWaterOutage(hass, entry, hass.data[DOMAIN][entry.entry_id])]
        )
    except Exception as e:
        _LOGGER.error(e)
    return False


class TavosWaterOutage(Entity):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, data):
        self._state = ""
        self._hass = hass
        self._all_outages = {}
        self._name = "tavos_water_outage_" + entry.data.get(MONITORED_STRING).lower()
        self._monitored_string = entry.data.get(MONITORED_STRING).lower()
        self._controller = data["controller"]
        self._coordinator = data["coordinator"]

        self.manualUpdate()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        await self._coordinator.async_request_refresh()
        self.manualUpdate()

    def manualUpdate(self):
        self._state = ""
        tavosData = self._hass.data[DOMAIN]["controller"].getData()
        self._all_outages = {}
        for waterOutage in tavosData:
            attribute = ""
            if "date" in waterOutage:
                if "start" in waterOutage["date"] and waterOutage["date"]["start"]:
                    attribute = attribute + waterOutage["date"]["start"].strftime(
                        "%d.%m.%Y %H:%M"
                    )
                if "end" in waterOutage["date"] and waterOutage["date"]["end"]:
                    attribute = (
                        attribute
                        + " - "
                        + waterOutage["date"]["end"].strftime("%d.%m.%Y %H:%M")
                    )

            value = ""
            if "city" in waterOutage and waterOutage["city"] != "":
                value = value + waterOutage["city"]
            if "street" in waterOutage and waterOutage["street"] != "":
                value = value + " (" + waterOutage["street"] + ")"
            if "waterImport" in waterOutage and waterOutage["waterImport"] != "":
                value = value + " - " + waterOutage["waterImport"]
            if "notes" in waterOutage and waterOutage["notes"] != "":
                value = value + " (" + waterOutage["notes"] + ")"
            if attribute != "" and value != "":
                self._all_outages[attribute] = value

            isMonitored = (
                self._monitored_string in waterOutage["city"].lower()
                or self._monitored_string in waterOutage["street"].lower()
            )
            isInFuture = (
                waterOutage["date"]["start"] != False
                and datetime.now() < waterOutage["date"]["start"]
            ) or (
                waterOutage["date"]["end"] != False
                and datetime.now() < waterOutage["date"]["end"]
            )

            if isMonitored and isInFuture:
                if self._state != "":
                    self._state = self._state + "\r\n" + attribute + ": " + value
                else:
                    self._state = attribute + ": " + value

    @property
    def device_state_attributes(self):
        return self._all_outages

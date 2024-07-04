from tavosPy import TavosPy
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN, _LOGGER


async def async_setup(hass: HomeAssistant, config: dict):
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["controller"] = TavosPy()

    def handleShutdown(event):
        """Clean up resources when shutting down."""

    try:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, handleShutdown)

        async def async_update_data():
            await hass.async_add_executor_job(hass.data[DOMAIN]["controller"].update)

        await hass.async_add_executor_job(hass.data[DOMAIN]["controller"].update)
        hass.data[DOMAIN]["coordinator"] = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name="Tavos resource status",
            update_method=async_update_data,
            update_interval=timedelta(seconds=120),
        )

        await hass.data[DOMAIN]["coordinator"].async_refresh()

    except Exception:
        _LOGGER.exception("Failed to set up Tavos Water Outage")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):

    hass.data[DOMAIN][entry.entry_id] = {
        "controller": hass.data[DOMAIN]["controller"],
        "coordinator": hass.data[DOMAIN]["coordinator"],
    }

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    )

    return True

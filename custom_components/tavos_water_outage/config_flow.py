import voluptuous as vol

from homeassistant import config_entries
from .const import DOMAIN, _LOGGER, MONITORED_STRING


@config_entries.HANDLERS.register(DOMAIN)
class FlowHandler(config_entries.ConfigFlow):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        return await self.async_step_add_monitored()

    async def async_step_add_monitored(self, user_input=None):
        errors = {}
        self.monitoredString = ""

        if user_input is not None:
            try:
                self.monitoredString = user_input[MONITORED_STRING]

                return self.async_create_entry(
                    title=self.monitoredString,
                    data={MONITORED_STRING: self.monitoredString,},
                )

            except Exception as e:
                errors["base"] = "unknown"
                _LOGGER.error(e)

        return self.async_show_form(
            step_id="add_monitored",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        MONITORED_STRING,
                        description={"suggested_value": self.monitoredString},
                    ): str,
                }
            ),
            errors=errors,
        )

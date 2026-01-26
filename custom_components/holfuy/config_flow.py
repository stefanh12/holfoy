import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from .const import (
    DOMAIN,
    CONF_STATION_IDS,
    CONF_WIND_UNIT,
    CONF_TEMP_UNIT,
    DEFAULT_WIND_UNIT,
    DEFAULT_TEMP_UNIT,
)

WIND_UNIT_OPTIONS = ["knots", "km/h", "m/s", "mph"]
TEMP_UNIT_OPTIONS = ["C", "F"]
MAX_STATIONS = 3


def _normalize_station_input(value: str):
    """Split comma-separated station ids, strip whitespace, drop empties, ensure max count."""
    parts = [p.strip() for p in value.split(",")]
    parts = [p for p in parts if p]
    if not parts:
        raise vol.Invalid("Please enter at least one station id")
    if len(parts) > MAX_STATIONS:
        raise vol.Invalid(f"Up to {MAX_STATIONS} stations are supported")
    return parts


class HolfuyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        """Handle the initial config flow."""
        if user_input is not None:
            # user_input[CONF_STATION_IDS] is a comma-separated string — store as a list
            station_input = user_input.pop(CONF_STATION_IDS)
            stations = _normalize_station_input(station_input)
            data = {**user_input, CONF_STATION_IDS: stations}
            return self.async_create_entry(title="Holfuy", data=data)

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_STATION_IDS, default=""): str,
                vol.Required(CONF_WIND_UNIT, default=DEFAULT_WIND_UNIT): vol.In(WIND_UNIT_OPTIONS),
                vol.Required(CONF_TEMP_UNIT, default=DEFAULT_TEMP_UNIT): vol.In(TEMP_UNIT_OPTIONS),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    def async_get_options_flow(config_entry):
        """Return options flow handler."""
        return HolfuyOptionsFlow(config_entry)


class HolfuyOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Store the provided config_entry without overwriting the base property."""
        super().__init__()
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options for the integration."""
        if user_input is not None:
            # Normalize stations input and update data
            station_input = user_input.pop(CONF_STATION_IDS)
            stations = _normalize_station_input(station_input)
            new_data = {**self._config_entry.data, **user_input, CONF_STATION_IDS: stations}
            self.hass.config_entries.async_update_entry(self._config_entry, data=new_data)
            return self.async_create_entry(title="", data={})

        # Prepare defaults
        existing = self._config_entry.data
        stations_default = ",".join(existing.get(CONF_STATION_IDS, []))

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY, default=existing.get(CONF_API_KEY, "")): str,
                vol.Required(CONF_STATION_IDS, default=stations_default): str,
                vol.Required(
                    CONF_WIND_UNIT,
                    default=existing.get(CONF_WIND_UNIT, DEFAULT_WIND_UNIT),
                ): vol.In(WIND_UNIT_OPTIONS),
                vol.Required(
                    CONF_TEMP_UNIT,
                    default=existing.get(CONF_TEMP_UNIT, DEFAULT_TEMP_UNIT),
                ): vol.In(TEMP_UNIT_OPTIONS),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
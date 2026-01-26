import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import aiohttp
import async_timeout

from .const import (
    DOMAIN,
    API_URL,
    CONF_API_KEY,
    CONF_STATION_ID,
    CONF_WIND_UNIT,
    CONF_TEMP_UNIT,
    DEFAULT_WIND_UNIT,
    DEFAULT_TEMP_UNIT,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    api_key = entry.data.get(CONF_API_KEY)
    station_id = entry.data.get(CONF_STATION_ID)

    # read units from entry (fall back to defaults)
    su = entry.data.get(CONF_WIND_UNIT, DEFAULT_WIND_UNIT)
    tu = entry.data.get(CONF_TEMP_UNIT, DEFAULT_TEMP_UNIT)

    async def async_update_data():
        url = API_URL.format(station=station_id, api_key=api_key, tu=tu, su=su)
        async with aiohttp.ClientSession() as session:
            try:
                async with async_timeout.timeout(10):
                    response = await session.get(url)
                    return await response.json()
            except Exception as err:
                raise UpdateFailed(f"Error fetching data: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Holfuy Weather",
        update_method=async_update_data,
        update_interval=timedelta(minutes=2),
    )

    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, ["sensor"])
    return True
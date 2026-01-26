import logging
import asyncio
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
    CONF_STATION_IDS,
    CONF_WIND_UNIT,
    CONF_TEMP_UNIT,
    DEFAULT_WIND_UNIT,
    DEFAULT_TEMP_UNIT,
)

_LOGGER = logging.getLogger(__name__)


def _make_update_method(api_key: str, station: str, tu: str, su: str):
    async def async_update_data():
        url = API_URL.format(station=station, api_key=api_key, tu=tu, su=su)
        async with aiohttp.ClientSession() as session:
            try:
                async with async_timeout.timeout(10):
                    response = await session.get(url)
                    return await response.json()
            except Exception as err:
                raise UpdateFailed(f"Error fetching data for station {station}: {err}")

    return async_update_data


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    api_key = entry.data.get(CONF_API_KEY)

    # Require station list; no legacy single-station compatibility
    stations = entry.data.get(CONF_STATION_IDS)
    if not stations:
        _LOGGER.error(
            "No station IDs configured for Holfuy entry %s — CONF_STATION_IDS is required", entry.entry_id
        )
        return False

    # read units from entry (fall back to defaults)
    su = entry.data.get(CONF_WIND_UNIT, DEFAULT_WIND_UNIT)
    tu = entry.data.get(CONF_TEMP_UNIT, DEFAULT_TEMP_UNIT)

    # For each station, create a coordinator
    coordinators = {}

    for station in stations:
        update_method = _make_update_method(api_key, station, tu, su)
        coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=f"Holfuy Weather {station}",
            update_method=update_method,
            update_interval=timedelta(minutes=2),
        )
        coordinators[str(station)] = coordinator

    # Run first refresh for all coordinators in parallel
    try:
        await asyncio.gather(
            *[co.async_config_entry_first_refresh() for co in coordinators.values()]
        )
    except Exception as err:
        _LOGGER.error("Failed first refresh for Holfuy stations: %s", err)
        # allow setup to continue; individual coordinators will retry per update_interval

    # Store coordinators dict under the entry id
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinators

    # Forward setup to platforms (preferred API). Use a fallback for older HA versions.
    platforms = ["sensor"]
    if hasattr(hass.config_entries, "async_forward_entry_setups"):
        await hass.config_entries.async_forward_entry_setups(entry, platforms)
    else:
        for platform in platforms:
            await hass.config_entries.async_forward_entry_setup(entry, platform)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload an entry: unload platforms and clear coordinators."""
    if hasattr(hass.config_entries, "async_unload_platforms"):
        unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    else:
        # older HA: no batch unload helper (best-effort)
        unload_ok = True

    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return unload_ok
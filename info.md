# Holfuy Weather Integration

Integrate **Holfuy weather station data** into Home Assistant.

## Features

- Real-time wind and temperature data from Holfuy weather stations
- Support for multiple stations (up to 3)
- Configurable units (m/s, knots, km/h, mph for wind; °C/°F for temperature)
- API validation during setup
- Automatic throttling on API errors
- 17+ language translations

## Setup

1. **Get an API key** from Holfuy (contact them via https://api.holfuy.com/)
2. Add the integration via **Settings → Devices & Services → Add Integration → Holfuy**
3. Enter your API key, station IDs, and preferred units
4. The integration validates your configuration automatically

**Note for Sweden/Scandinavia**: Select **m/s** for wind speed during setup to match local conventions.

## Sensors Created

For each station:

- Wind Speed
- Wind Gust
- Wind Min
- Wind Direction
- Temperature

## Credits

Integration developed for the paragliding and outdoor sports community.

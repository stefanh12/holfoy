
# Holfuy Weather Integration for Home Assistant

This custom component integrates **Holfuy weather station data** into Home Assistant using the Holfuy API.

## Features
- Fetches real-time data from Holfuy stations:
  - Wind Speed
  - Wind Gust
  - Wind Min
  - Wind Direction
  - Temperature
- Includes station name and last update timestamp as attributes.
- Uses **DataUpdateCoordinator** for efficient updates.

## Installation via HACS
1. Go to **HACS → Integrations → Custom Repositories**.
2. Add your repository URL:  
   `https://github.com/stefanh12/holfuy-homeassistant`
3. Select **Integration**.
4. Restart Home Assistant.
5. Install the integration via HACS.

## Manual Installation
1. Copy `custom_components/holfuy` to your Home Assistant `custom_components` folder.
2. Restart Home Assistant.

## Configuration
1. Go to **Settings → Devices & Services → Add Integration → Holfuy**.
2. Enter:
   - **API Key** (from Holfuy)
   - **Station ID** (e.g., `601`)

## Example Sensors
- `sensor.holfuy_wind_speed`
- `sensor.holfuy_temperature`

## 🌍 Lovelace Dashboard Example

You can visualize wind direction and speed using the https://github.com/custom-cards/compass-card in your Lovelace dashboard.

### Example YAML:
```yaml
type: custom:compass-card
header:
title:
 value: Wind
indicator_sensors:
- sensor: sensor.holfuy_station_direction
 indicator:
   image: arrow_inward
value_sensors:
- sensor: sensor.holfuy_station_speed
- sensor: sensor.holfuy_station_gust

## Credits
Developed for Home Assistant using Holfuy API.

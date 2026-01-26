DOMAIN = "holfuy"
CONF_STATION_IDS = "station_ids"    # list of station ids (stored as list in entry.data)
CONF_API_KEY = "api_key"

# Config keys for units
CONF_WIND_UNIT = "wind_unit"
CONF_TEMP_UNIT = "temp_unit"

# Defaults
DEFAULT_WIND_UNIT = "m/s"   # options: "knots", "km/h", "m/s", "mph"
DEFAULT_TEMP_UNIT = "C"     # options: "C", "F"

# API URL accepts placeholders for tu and su
API_URL = "http://api.holfuy.com/live/?s={station}&pw={api_key}&m=JSON&tu={tu}&su={su}"

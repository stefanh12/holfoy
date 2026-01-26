DOMAIN = "holfuy"
CONF_STATION_ID = "station_id"
CONF_API_KEY = "api_key"

# New config keys for units
CONF_WIND_UNIT = "wind_unit"
CONF_TEMP_UNIT = "temp_unit"

# Defaults
DEFAULT_WIND_UNIT = "m/s"   # options: "knots", "km/h", "m/s", "mph"
DEFAULT_TEMP_UNIT = "C"     # options: "C", "F"

# API URL now accepts placeholders for tu and su
API_URL = "http://api.holfuy.com/live/?s={station}&pw={api_key}&m=JSON&tu={tu}&su={su}"

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class CityNotFoundError(Exception):
    """Se lanza cuando la geo9codificacion no devuelve resultados."""

class WeatherServiceError(Exception):
    """Se lanza cuando Open-Meteo falla, tarda o responde mal."""

async def get_current_weather(city: str) -> dict: 
    cleaned_city = city.strip()
    if not cleaned_city:
        raise CityNotFoundError("El nombre de la ciudad no puede estar vacio")

    timeout = httpx.Timeout(6.0, connect=3.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            geo_res = await client.get(
                GEOCODING_URL,
                params={"name": cleaned_city, "count": 1, "language": "es"},
            )
            geo_res.raise_for_status()
            geo_data = geo_res.json()

            results = geo_data.get("results") or []
            if not results:
                raise CityNotFoundError(f"No se encontro la ciudad '{cleaned_city}'.")

            place = results[0]
            lat = place["latitude"]
            lon = place["longitude"]

            weather_res = await client.get(
                FORECAST_URL,
                params={         
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,precipitation,wind_speed_10m",
                },
            )

            weather_res.raise_for_status()
            weather_data = weather_res.json()

    except CityNotFoundError:
        raise
    except httpx.TimeoutException as exc:
        raise WeatherServiceError("Tiempo de espera agotado al consultar Open-Meteo.") from exc
    except (httpx.HTTPError, KeyError, ValueError) as exc:
        raise WeatherServiceError("Error al obtener o interpretar datos del clima ")

    current = weather_data.get("current") or {}
    return {
        "city" : place.get("name", cleaned_city),
        "country": place.get("country"),
        "latitude": lat,
        "longitude": lon,
        "temperature_c": current.get("temperature_2m"),
        "precipitation_mm": current.get("precipitation"),
        "wind_kmh" : current.get("wind_speed_10m"),
    } 
from fastapi import FastAPI, HTTPException, Query

from app.rules import ActivityType, evaluate_activity
from app.weather_client import CityNotFoundError, WeatherServiceError, get_current_weather


app = FastAPI(title="Clima y Ventana de Actividad API", version="0.1.0")

@app.get("/healt")
def healtcheck():
        return {"status": "ok"}


@app.get("/api/window")
async def activity_window(
        city: str = Query(..., min_length=1, description="Nombre de la ciudad, ej. Trujillo "),
        activity: ActivityType = Query("walking", description="Actividad: running, walking o cycling"),
):
        try:
            weather = await get_current_weather(city)
        except CityNotFoundError as exc:
               raise HTTPException(status_code= 404, detail=str(exc)) from exc
        except WeatherServiceError as exc:
               raise HTTPException(status_code=502, detail=str(exc)) from exc

        temp= weather["temperature_c"]
        rain = weather["precipitation_mm"]
        wind = weather["wind_kmh"]

        if temp is None or rain is None or wind is None:
               raise HTTPException(status_code=502, detail="Datos metereologicos incompletos desde Open_Mateo ")

        status, reason = evaluate_activity(activity, temp, rain, wind)

        return {
        "location": {
            "city": weather["city"],
            "country": weather["country"],
            "latitude": weather["latitude"],
            "longitude": weather["longitude"],
        },
        "activity": activity,
        "weather": {
            "temperature_c": temp,
            "precipitation_mm": rain,
            "wind_kmh": wind,
        },
        "assessment": {
            "status": status,
            "reason": reason,
        },
    }

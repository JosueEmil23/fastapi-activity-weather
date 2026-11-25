from typing import Literal

StatusType = Literal["ideal", "aceptable", "eviatr"]
ActivityType = Literal["running", "walking", "cycling"]


def evaluate_activity(activity: ActivityType, temp_c: float, rain_mm: float, wind_kmh: float) -> tuple[StatusType, str]: 

    if rain_mm >= 2.0:
        return "evitar", f"Hay lluvia notable({rain_mm} mm) en este momento"

    if rain_mm > 0.0:
        return "aceptable", f"Hay llovizna o lluvia ligera({rain_mm} mm); convienellevar abrigo impermeable "

    if activity == "cycling":
        if wind_kmh >= 30:
            return "evitar", f"Viento fuerte ({wind_kmh} km/h) poco seguro o incomodo para ciclismo"
        if wind_kmh >=18 or temp_c < 10 or temp_c > 33: 
            return "aceptable", f"Buen clima para salir en bici ({temp_c}°C, viento: {wind_kmh} km/h)"

    if activity == "running":
        if temp_c >= 34 or wind_kmh>= 35:
                    return "evitar", f"Condiciones exigentes para correr ({temp_c}°C, viento: {wind_kmh} km/h)"
        if temp_c >=28 or temp_c < 8 or wind_kmh > 22: 
                    return "ideal", f" Temperatura y viento favorables para correr ({temp_c}°C, viento: {wind_kmh} km/h)"

    if temp_c >= 36 or wind_kmh >= 40:
          return "evitar", f"Clima adverso para caminar ({temp_c}°C, viento:{wind_kmh} km/h)"
    if temp_c > 31 or temp_c < 7 or wind_kmh >=25:
          return "aceptable", f"Caminata posible con ajustes de ropa o hidratacion ({temp_c}°C, viento: {wind_kmh} km/h)"
    return "ideal", f"Buen momento para salir a caminar ({temp_c}°C, viento: {wind_kmh} km/h)"

    


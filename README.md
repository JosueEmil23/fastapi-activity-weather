<div align="center">

# fastapi-activity-weather

<p>
  <strong>API REST con FastAPI, httpx y Uvicorn para evaluar ventanas de actividades al aire libre según el clima actual de Open-Meteo.</strong>
</p>

<p>
  <code>Python</code> · <code>FastAPI</code> · <code>httpx</code> · <code>Open-Meteo</code> · <code>REST API</code>
</p>

</div>

<hr />

<h2>¿Qué hace esta API?</h2>

<p>
  Consulta las condiciones meteorológicas actuales de una ciudad a través de <strong>Open-Meteo</strong> (sin necesidad de API keys) y evalúa si el entorno es <code>ideal</code>, <code>aceptable</code> o <code>evitar</code> para actividades como <code>walking</code>, <code>running</code> o <code>cycling</code>.
</p>

<table>
  <thead>
    <tr>
      <th>Estado</th>
      <th>Significado</th>
      <th>Criterio general</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>ideal</code></td>
      <td>Condiciones favorables</td>
      <td>Sin lluvia relevante y con temperatura y viento cómodos para la actividad.</td>
    </tr>
    <tr>
      <td><code>aceptable</code></td>
      <td>Viable con precaución</td>
      <td>Llovizna ligera o valores moderados de calor/frío/viento que requieren ajustes.</td>
    </tr>
    <tr>
      <td><code>evitar</code></td>
      <td>Condiciones adversas</td>
      <td>Lluvia notable o rangos extremos de temperatura/viento para la actividad elegida.</td>
    </tr>
  </tbody>
</table>

<h2>Arquitectura</h2>

<pre><code>Clima-api/
├── app/
│   ├── main.py            # Rutas FastAPI (/health, /api/window) y manejo de errores HTTP
│   ├── weather_client.py  # Cliente asíncrono con httpx hacia Open-Meteo (geocoding + forecast)
│   └── rules.py           # Reglas de evaluación por actividad (walking, running, cycling)
├── requirements.txt       # Dependencias directas del proyecto
├── .gitignore             # Exclusión de entornos virtuales y archivos temporales
└── README.md              # Documentación del repositorio
</code></pre>

<details>
  <summary><strong>Ver flujo interno de <code>GET /api/window</code></strong></summary>
  <ol>
    <li>Valida los parámetros de consulta <code>city</code> (requerido) y <code>activity</code> (<code>walking</code>, <code>running</code> o <code>cycling</code>; por defecto <code>walking</code>).</li>
    <li><code>weather_client.py</code> resuelve la ciudad a <code>latitude</code> y <code>longitude</code> en Open-Meteo Geocoding y consulta <code>temperature_2m</code>, <code>precipitation</code> y <code>wind_speed_10m</code> en Open-Meteo Forecast.</li>
    <li><code>rules.py</code> evalúa las métricas según la actividad y devuelve el estado y el motivo.</li>
    <li><code>main.py</code> retorna la respuesta JSON estructurada.</li>
  </ol>
</details>

<h2>Instalación y ejecución</h2>

<pre><code>git clone https://github.com/TU_USUARIO/fastapi-activity-weather.git
cd fastapi-activity-weather

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python -m uvicorn app.main:app --reload
</code></pre>

<p>
  Una vez levantado el servidor, puedes consultar <code>http://127.0.0.1:8000/health</code> o abrir la documentación interactiva en <code>http://127.0.0.1:8000/docs</code>.
</p>

<h2>Ejemplo de petición y respuesta</h2>

<p><strong>Petición:</strong></p>

<pre><code>GET /api/window?city=Trujillo&amp;activity=walking HTTP/1.1
Host: 127.0.0.1:8000
</code></pre>

<p><strong>Respuesta (<code>200 OK</code>):</strong></p>

<pre><code>{
  "location": {
    "city": "Trujillo",
    "country": "Perú",
    "latitude": -8.11599,
    "longitude": -79.02998
  },
  "activity": "walking",
  "weather": {
    "temperature_c": 27.5,
    "precipitation_mm": 0.0,
    "wind_kmh": 13.5
  },
  "assessment": {
    "status": "ideal",
    "reason": "Buen momento para caminar (27.5°C, viento: 13.5 km/h)."
  }
}
</code></pre>

<p><strong>Códigos de error:</strong> <code>404</code> si no se encuentra la ciudad, <code>422</code> si faltan o fallan parámetros de consulta y <code>502</code> ante fallos o datos incompletos de Open-Meteo.</p>

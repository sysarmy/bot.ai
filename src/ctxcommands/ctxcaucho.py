import requests
import discord
from datetime import datetime
import json
from ratelimit import limits
from bs4 import BeautifulSoup

quince_minutos = 900

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def cauchofunctx(ctx):

    FechaActual = datetime.now()
    CAUCIONES_IOL_URL = "https://iol.invertironline.com/mercado/cotizaciones/argentina/cauciones"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "es-AR,es;q=0.9"
    }

    try:
        r = requests.get(CAUCIONES_IOL_URL, headers=HEADERS, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        tabla = soup.find("table", {"id": "cotizaciones"})
            
        if not tabla:
            print("No se encontró la tabla de cotizaciones.")
            return


        # Log
        print(FechaActual)
        print(f"Se ha ejecutado el comando !caucho por {ctx.author}")

        cauciones = []
        for fila in tabla.find("tbody").find_all("tr"):
            columnas = fila.find_all("td")
            if len(columnas) < 6:
                continue

            moneda = columnas[1].text.strip()
            if moneda != "PESOS":
                continue

            plazo_tag = columnas[0].find("strong")
            if not plazo_tag:
                continue
            plazo = int(plazo_tag.text.strip())

            # columnas[5] = "Tasa Tomadora" (el segundo td.tac)
            tasa_raw = columnas[5].get("data-order", "").replace(",", ".")
            if not tasa_raw:
                continue

            tasa = float(tasa_raw)
            if tasa == 0:
                continue  # filas sin tasa real

            cauciones.append({"dias": plazo, "tasa": tasa})

        if not cauciones:                
            print("No se encontraron cauciones en pesos con tasa válida.")
            return

        cauciones = sorted(cauciones, key=lambda x: x["dias"])[:3]

        mensaje = "📊 Cauciones en PESOS\n"

        for c in cauciones:
            mensaje += f"{c['dias']} días --> TNA: {c['tasa']} %\n"
        
        await ctx.send(mensaje)

    except Exception as e:
        print(f"Error en la web: {e}")
        await ctx.send(f"Error. Pincho la API. Error")
    
    


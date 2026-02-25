import requests
import discord
from discord import Embed
from datetime import datetime
from bs4 import BeautifulSoup
from ratelimit import limits

quince_minutos = 900

@limits(calls=15, period=quince_minutos)
async def cauchofun(interaction):

    FechaActual = datetime.now()

    try:
        url = "https://iol.invertironline.com/mercado/cotizaciones/argentina/cauciones"

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")
            tabla = soup.find("table", {"id": "cotizaciones"})

            if not tabla:
                print("No se encontró tabla (mercado cerrado?)")
                return

            filas = tabla.find("tbody").find_all("tr")

            cauciones = []

            for fila in filas:

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

                tasa_raw = columnas[5].get("data-order")
                if not tasa_raw:
                    continue

                tasa = float(tasa_raw.replace(",", "."))

                if tasa == 0:
                    continue

                cauciones.append({
                    "dias": plazo,
                    "tasa": tasa
                })

            if not cauciones:
                print("No se encontraron cauciones en PESOS")
                return

            # Ordenamos por plazo y tomamos las primeras 10
            cauciones = sorted(cauciones, key=lambda x: x["dias"])[:10]

            # LOG
            print(FechaActual)
            print(f"Se ha ejecutado el comando caucho por {interaction.user}")

            # Crear embed igual estilo que dolarfun
            embed = Embed(
                title="📊 Tasas de Caución en PESOS",
                description=f"A pedido de {interaction.user}",
                color=discord.Color.green()
            )

            for c in cauciones:
                embed.add_field(
                    name=f"{c['dias']} días",
                    value=f"TNA = {c['tasa']} %",
                    inline=False
                )

            return embed

        else:
            print(f"Error: {response.status_code}. Pinchó IOL.")

    except Exception as e:
        print(f"Error en cauciones: {e}")

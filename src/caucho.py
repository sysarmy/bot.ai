import aiohttp
import asyncio
import discord
from discord import Embed
from bs4 import BeautifulSoup
from datetime import datetime


async def caucho(interaction: discord.Interaction, monto: float = None):
    await interaction.response.defer()

    url = "https://iol.invertironline.com/mercado/cotizaciones/argentina/cauciones"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "es-AR,es;q=0.9"
    }

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await interaction.followup.send("❌ No se pudo consultar IOL.")
                    return
                html = await response.text()

        soup = BeautifulSoup(html, "html.parser")
        tabla = soup.find("table", {"id": "cotizaciones"})

        if not tabla:
            await interaction.followup.send("📴 Mercado posiblemente cerrado o sin datos.")
            return

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
            await interaction.followup.send("📴 No se encontraron cauciones en PESOS.")
            return

        cauciones = sorted(cauciones, key=lambda x: x["dias"])[:10]

        embed = Embed(
            title="📊 Cauciones en PESOS",
            description=f"Solicitado por {interaction.user}",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"IOL • {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        if monto is None:
            for c in cauciones:
                embed.add_field(
                    name=f"{c['dias']} días",
                    value=f"TNA: {c['tasa']} %",
                    inline=True
                )
        else:
            for c in cauciones:
                dias = c["dias"]
                tasa = c["tasa"]
                interes = monto * (tasa / 100) * (dias / 365)
                monto_final = monto + interes
                embed.add_field(
                    name=f"{dias} días • {tasa}%",
                    value=(
                        f"Invertido: ${monto:,.0f}\n"
                        f"Interés: ${interes:,.2f}\n"
                        f"Final: ${monto_final:,.2f}"
                    ),
                    inline=False
                )

        await interaction.followup.send(embed=embed)
        print(f"{datetime.now()} - /caucho ejecutado por {interaction.user}")

    except asyncio.TimeoutError:
        await interaction.followup.send("⏳ Timeout consultando IOL.")
    except Exception as e:
        print(f"Error en /caucho: {e}")
        await interaction.followup.send("⚠️ Error procesando la caución.")

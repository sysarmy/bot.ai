import requests
import discord
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_cauciones_iol():
    url = "https://iol.invertironline.com/mercado/cotizaciones/argentina/cauciones"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "es-AR,es;q=0.9"
    }
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    tabla = soup.find("table", {"id": "cotizaciones"})
    if not tabla:
        return None

    cauciones = []
    for fila in tabla.find("tbody").find_all("tr"):
        columnas = fila.find_all("td")
        if len(columnas) < 6:
            continue
        if columnas[1].text.strip() != "PESOS":
            continue
        plazo_tag = columnas[0].find("strong")
        if not plazo_tag:
            continue
        tasa_raw = columnas[5].get("data-order", "").replace(",", ".")
        if not tasa_raw:
            continue
        tasa = float(tasa_raw)
        if tasa == 0:
            continue
        cauciones.append({"dias": int(plazo_tag.text.strip()), "tasa": tasa})

    return sorted(cauciones, key=lambda x: x["dias"])[:10]


async def cauchofunctx(ctx, monto=None):
    FechaActual = datetime.now()
    print(f"{FechaActual} - Se ejecutó el comando caucho")

    try:
        cauciones = fetch_cauciones_iol()

        if not cauciones:
            await ctx.send("📴 Mercado cerrado o sin datos de cauciones.")
            return

        if monto is None:
            mensaje = "📊 **Cauciones en PESOS**\n"
            for c in cauciones:
                mensaje += f"{c['dias']}D → TNA {c['tasa']}%\n"
            await ctx.send(mensaje)

        else:
            monto = float(monto)
            mensaje = f"📊 **Cauciones en PESOS para ${monto:,.0f}**\n"
            for c in cauciones:
                interes = monto * (c["tasa"] / 100) * (c["dias"] / 365)
                monto_final = monto + interes
                mensaje += f"{c['dias']}D • {c['tasa']}% → Interés: ${interes:,.2f} | Final: ${monto_final:,.2f}\n"
            await ctx.send(mensaje)

    except Exception as e:
        print(f"Error en /caucho: {e}")
        await ctx.send("⚠️ Error consultando cauciones.")

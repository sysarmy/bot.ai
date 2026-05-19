import datetime
import os

import requests


# ID de liga y temporada para la Copa del Mundo FIFA 2026 en api-football
MUNDIAL_LEAGUE_ID = 1
MUNDIAL_SEASON = 2026


async def mundialfunctx(ctx):
    """Comando !mundial (ctx): responde en texto plano para IRC/bridge."""
    try:
        apisports_key = os.getenv("APISPORTS_KEY")
        if not apisports_key:
            await ctx.send("Error: No se encontro APISPORTS_KEY en el .env")
            return

        hoy = datetime.date.today().strftime("%Y-%m-%d")
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {"x-apisports-key": apisports_key}
        params = {
            "league": MUNDIAL_LEAGUE_ID,
            "season": MUNDIAL_SEASON,
            "date": hoy,
            "timezone": "America/Argentina/Buenos_Aires",
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        partidos = data.get("response", [])

        print(f"{datetime.datetime.now()} - Se ejecuto el comando !mundial")

        if not partidos:
            await ctx.send(f"🏆 Mundial 2026 - {hoy}: no hay partidos programados para hoy.")
            return

        mensaje = f"🏆 Mundial 2026 - Partidos del {hoy}\n"
        estados_en_juego = {"1H", "HT", "2H", "ET", "BT", "P", "INT", "LIVE"}
        estados_finalizado = {"FT", "AET", "PEN", "AWD", "WO"}

        for partido in partidos:
            equipo_local = partido["teams"]["home"]["name"]
            equipo_visitante = partido["teams"]["away"]["name"]
            estado = partido["fixture"]["status"]["short"]
            fecha_iso = partido["fixture"]["date"]
            ronda = partido["league"].get("round", "")

            try:
                dt = datetime.datetime.fromisoformat(fecha_iso)
                hora = dt.strftime("%H:%M")
            except Exception:
                hora = "??:??"

            goles_local = partido["goals"]["home"]
            goles_visitante = partido["goals"]["away"]

            if estado in estados_finalizado:
                resultado = f"{goles_local}-{goles_visitante} Final"
            elif estado in estados_en_juego:
                elapsed = partido["fixture"]["status"].get("elapsed", "")
                resultado = f"{goles_local}-{goles_visitante} {elapsed}'"
            elif estado == "NS":
                resultado = f"{hora} hs"
            elif estado in {"PST", "CANC", "SUSP", "ABD"}:
                resultado = f"Suspendido/Postergado ({estado})"
            else:
                resultado = hora

            ronda_txt = f" [{ronda}]" if ronda else ""
            mensaje += f"{equipo_local} vs {equipo_visitante}: {resultado}{ronda_txt}\n"

        await ctx.send(mensaje.strip())

    except Exception as e:
        print(f"Error en !mundial: {e}")
        await ctx.send("Error al consultar los partidos del Mundial. Intenta mas tarde.")

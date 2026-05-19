import discord
from discord import Embed
import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# ID de liga y temporada para la Copa del Mundo FIFA 2026 en api-football
MUNDIAL_LEAGUE_ID = 1
MUNDIAL_SEASON = 2026

async def mundialfun(interaction):
    try:
        APISPORTS_KEY = os.getenv('APISPORTS_KEY')
        if not APISPORTS_KEY:
            embed = Embed(
                title="🏆 Copa del Mundo FIFA 2026",
                description="Error: No se encontro la API key. Configura APISPORTS_KEY en el .env",
                color=discord.Color.red()
            )
            return embed

        hoy = datetime.date.today().strftime("%Y-%m-%d")

        url = "https://v3.football.api-sports.io/fixtures"
        headers = {
            'x-apisports-key': APISPORTS_KEY,
        }
        params = {
            'league': MUNDIAL_LEAGUE_ID,
            'season': MUNDIAL_SEASON,
            'date': hoy,
            'timezone': 'America/Argentina/Buenos_Aires',
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        # Log
        print(f"{datetime.datetime.now()} - Se ejecuto el comando /mundial")

        partidos = data.get("response", [])

        embed = Embed(
            title="🏆 Copa del Mundo FIFA 2026",
            description=f"Partidos del {hoy}",
            color=discord.Color.gold()
        )

        if not partidos:
            embed.add_field(
                name="Sin partidos",
                value="No hay partidos programados para hoy.",
                inline=False
            )
            return embed

        for partido in partidos:
            equipo_local = partido["teams"]["home"]["name"]
            equipo_visitante = partido["teams"]["away"]["name"]
            estado = partido["fixture"]["status"]["short"]
            fecha_iso = partido["fixture"]["date"]
            ronda = partido["league"].get("round", "")

            # Parseamos la hora del partido
            try:
                dt = datetime.datetime.fromisoformat(fecha_iso)
                hora = dt.strftime("%H:%M")
            except Exception:
                hora = "??:??"

            # Mostramos el marcador segun el estado del partido
            goles_local = partido["goals"]["home"]
            goles_visitante = partido["goals"]["away"]

            estados_en_juego = {"1H", "HT", "2H", "ET", "BT", "P", "INT", "LIVE"}
            estados_finalizado = {"FT", "AET", "PEN", "AWD", "WO"}

            if estado in estados_finalizado:
                resultado = f"{goles_local} - {goles_visitante} (Final)"
            elif estado in estados_en_juego:
                elapsed = partido["fixture"]["status"].get("elapsed", "")
                resultado = f"{goles_local} - {goles_visitante} ({elapsed}')"
            elif estado == "NS":
                resultado = f"{hora} hs"
            elif estado in {"PST", "CANC", "SUSP", "ABD"}:
                resultado = f"Suspendido/Postergado ({estado})"
            else:
                resultado = hora

            embed.add_field(
                name=f"⚽ {equipo_local} vs {equipo_visitante}",
                value=f"{resultado}\n_{ronda}_",
                inline=False
            )

        return embed

    except Exception as e:
        print(f"Error en mundialfun: {e}")
        embed = Embed(
            title="🏆 Copa del Mundo FIFA 2026",
            description="Error al consultar los partidos. Intenta mas tarde.",
            color=discord.Color.red()
        )
        return embed

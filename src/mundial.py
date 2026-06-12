import discord
from discord import Embed
import json
import http.client
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Codigo de competencia para FIFA World Cup en football-data.org
MUNDIAL_COMPETITION_CODE = "WC"

async def mundialfun(interaction):
    try:
        fulbo_token = os.getenv("FULBO_token")
        if not fulbo_token:
            embed = Embed(
                title="🏆 Copa del Mundo FIFA 2026",
                description="Error: No se encontro la API key. Configura FULBO_token en el .env",
                color=discord.Color.red()
            )
            return embed

        hoy = datetime.date.today()
        hoy_string = hoy.strftime("%Y-%m-%d")

        connection = http.client.HTTPSConnection("api.football-data.org")
        headers = {"X-Auth-Token": f"{fulbo_token}"}
        connection.request(
            "GET",
            f"/v4/competitions/{MUNDIAL_COMPETITION_CODE}/matches?dateFrom={hoy_string}&dateTo={hoy_string}",
            None,
            headers,
        )
        api_response = connection.getresponse()
        raw_body = api_response.read().decode("utf-8", errors="replace")

        if api_response.status != 200:
            error_embed = Embed(
                title="🏆 Copa del Mundo FIFA 2026",
                description=f"Error API football-data ({api_response.status}). Intenta mas tarde.",
                color=discord.Color.red(),
            )
            return error_embed

        if not raw_body.strip():
            error_embed = Embed(
                title="🏆 Copa del Mundo FIFA 2026",
                description="La API devolvio una respuesta vacia. Intenta mas tarde.",
                color=discord.Color.red(),
            )
            return error_embed

        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError:
            error_embed = Embed(
                title="🏆 Copa del Mundo FIFA 2026",
                description="La API devolvio una respuesta invalida. Intenta mas tarde.",
                color=discord.Color.red(),
            )
            return error_embed

        # Log
        print(f"{datetime.datetime.now()} - Se ejecuto el comando /mundial")

        partidos = data.get("matches", [])
        competition_name = data.get("competition", {}).get("name", "Copa del Mundo FIFA")

        embed = Embed(
            title=f"🏆 {competition_name}",
            description=f"Partidos del {hoy_string}",
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
            equipo_local = partido["homeTeam"]["name"]
            equipo_visitante = partido["awayTeam"]["name"]
            estado = partido.get("status", "")
            fecha_iso = partido.get("utcDate", "")
            ronda = partido.get("stage", "")
            matchday = partido.get("matchday")

            # Parseamos la hora del partido
            try:
                dt = datetime.datetime.fromisoformat(fecha_iso.replace("Z", "+00:00"))
                hora = dt.strftime("%H:%M UTC")
            except Exception:
                hora = "??:??"

            # Mostramos el marcador segun el estado del partido
            goles_local = partido.get("score", {}).get("fullTime", {}).get("home")
            goles_visitante = partido.get("score", {}).get("fullTime", {}).get("away")
            goles_local_txt = "-" if goles_local is None else goles_local
            goles_visitante_txt = "-" if goles_visitante is None else goles_visitante

            estados_en_juego = {"IN_PLAY", "PAUSED", "EXTRA_TIME", "PENALTY_SHOOTOUT"}
            estados_finalizado = {"FINISHED", "AWARDED"}
            estado_suspendido = {"POSTPONED", "SUSPENDED", "CANCELLED"}

            if estado in estados_finalizado:
                resultado = f"{goles_local_txt} - {goles_visitante_txt} (Final)"
            elif estado in estados_en_juego:
                resultado = f"{goles_local_txt} - {goles_visitante_txt} (En juego)"
            elif estado == "SCHEDULED":
                resultado = f"{hora} hs"
            elif estado in estado_suspendido:
                resultado = f"Suspendido/Postergado ({estado})"
            else:
                resultado = hora

            detalle_fecha = f" - Fecha {matchday}" if matchday is not None else ""

            embed.add_field(
                name=f"⚽ {equipo_local} vs {equipo_visitante}",
                value=f"{resultado}\n_{ronda}{detalle_fecha}_",
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

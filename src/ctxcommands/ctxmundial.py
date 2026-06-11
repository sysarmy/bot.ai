import datetime
import os
import json
import http.client

from dotenv import load_dotenv


load_dotenv()
MUNDIAL_COMPETITION_CODE = "WC"


async def mundialfunctx(ctx):
    """Comando !mundial (ctx): responde en texto plano para IRC/bridge."""
    try:
        fulbo_token = os.getenv("FULBO_token")
        if not fulbo_token:
            await ctx.send("Error: No se encontro FULBO_token en el .env")
            return

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
            await ctx.send(f"Error API football-data ({api_response.status}). Intenta mas tarde.")
            return

        if not raw_body.strip():
            await ctx.send("La API devolvio una respuesta vacia. Intenta mas tarde.")
            return

        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError:
            await ctx.send("La API devolvio una respuesta invalida. Intenta mas tarde.")
            return
        partidos = data.get("matches", [])
        competition_name = data.get("competition", {}).get("name", "Copa del Mundo FIFA")

        print(f"{datetime.datetime.now()} - Se ejecuto el comando !mundial")

        if not partidos:
            await ctx.send(f"🏆 {competition_name} - {hoy_string}: no hay partidos programados para hoy.")
            return

        mensaje = f"🏆 {competition_name} - Partidos del {hoy_string}\n"
        estados_en_juego = {"IN_PLAY", "PAUSED", "EXTRA_TIME", "PENALTY_SHOOTOUT"}
        estados_finalizado = {"FINISHED", "AWARDED"}
        estado_suspendido = {"POSTPONED", "SUSPENDED", "CANCELLED"}

        for partido in partidos:
            equipo_local = partido["homeTeam"]["name"]
            equipo_visitante = partido["awayTeam"]["name"]
            estado = partido.get("status", "")
            fecha_iso = partido.get("utcDate", "")
            ronda = partido.get("stage", "")
            matchday = partido.get("matchday")

            try:
                dt = datetime.datetime.fromisoformat(fecha_iso.replace("Z", "+00:00"))
                hora = dt.strftime("%H:%M UTC")
            except Exception:
                hora = "??:??"

            goles_local = partido.get("score", {}).get("fullTime", {}).get("home")
            goles_visitante = partido.get("score", {}).get("fullTime", {}).get("away")
            goles_local_txt = "-" if goles_local is None else goles_local
            goles_visitante_txt = "-" if goles_visitante is None else goles_visitante

            if estado in estados_finalizado:
                resultado = f"{goles_local_txt}-{goles_visitante_txt} Final"
            elif estado in estados_en_juego:
                resultado = f"{goles_local_txt}-{goles_visitante_txt} En juego"
            elif estado == "SCHEDULED":
                resultado = f"{hora} hs"
            elif estado in estado_suspendido:
                resultado = f"Suspendido/Postergado ({estado})"
            else:
                resultado = hora

            ronda_txt = f" [{ronda}]" if ronda else ""
            fecha_txt = f" [Fecha {matchday}]" if matchday is not None else ""
            mensaje += f"{equipo_local} vs {equipo_visitante}: {resultado}{ronda_txt}{fecha_txt}\n"

        await ctx.send(mensaje.strip())

    except Exception as e:
        print(f"Error en !mundial: {e}")
        await ctx.send("Error al consultar los partidos del Mundial. Intenta mas tarde.")

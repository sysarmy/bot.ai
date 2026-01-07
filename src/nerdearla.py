import discord
from discord import Embed
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from ratelimit import limits
import requests

#########################################################################################
############ FUNCION PARA BUSCAR CHARLAS EN YOUTUBE Y CALENDAR DE NERDEARLA #############
#########################################################################################
quince_minutos = 900
load_dotenv()

@limits(calls=5, period=quince_minutos)
async def nerdearlacharlasfunc(interaction, texto):

    # Hacemos un defer para darle tiempo al bot y poder mandar dos respuestas de embed
    await interaction.response.defer(ephemeral=True) 

    FechaActual = datetime.now()

    ###################### Setup y llamado a la API de Google para YouTube y para el Google Calendar ######################
    YOUTUBE_API_KEY = os.getenv('google_key')
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    channel_id = 'UC1WxOSF0QFb7C0I_QGiDlrA'  # Channel ID de Nerdearla

    ###################### Bloque de busqueda en Endpoint de backstage ######################

    # Conecta al endpoint de nerdearla y trae JSON
    API_URL = "https://backstage.nerdearla.com/api/sessions/"
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    data = response.json()
    sessions = data.get("sessions", [])
    lista_charlas = []

    # Buscamos las charlas por titulo
    for session in sessions:
        title = session.get("title", "")
        if texto.lower() not in title.lower():
            continue

        # Chequeamos solo por charlas en el futuro
        start_raw = session.get("start")

        if not start_raw:
            continue
        try:
            session_date = datetime.strptime(start_raw, "%Y-%m-%d %H:%M")
        except ValueError:
            continue
        if session_date < datetime.now():
            continue

        fecha_str = start_raw

        # Trae data de speakers
        speaker_entries = session.get("speakers", [])
        speaker_names = []

        for sp in speaker_entries:
            if isinstance(sp, dict):
                first = sp.get("first_name", "")
                last = sp.get("last_name", "")
                full_name = f"{first} {last}".strip()
                if full_name:
                    speaker_names.append(full_name)

        speakers_str = ", ".join(speaker_names) or "Speaker no disponible"


        lista_charlas.append({
            "title": title,
            "start": fecha_str,
            "speakers": speakers_str
        })

    # Limitamos a 5 resultados
    lista_charlas = lista_charlas[:5]

    # Crea el embed para mandar
    if lista_charlas:
        embedCharlas = discord.Embed(title="Próximas charlas en Nerdearla (5 max)", color=discord.Color.blue())

        for event in lista_charlas:
            embedCharlas.add_field(
                name=event["title"],
                value=(
                    f" **Fecha y Hora:** {event['start']}\n"
                    f" **Speakers:** {event['speakers']}"
                ),
                inline=False
            )

        await interaction.followup.send(embed=embedCharlas, ephemeral=True)
    else:
        await interaction.followup.send(
            f"No encontré charlas próximas en Nerdearla para '{texto}'",
            ephemeral=True
        )

    ###################### Bloque de busqueda en YouTube ######################

    # Buscamos video por el titulo
    search_response = youtube.search().list(
        q=texto,
        part='snippet',
        channelId=channel_id,
        maxResults=5,  # Limitamos a un maximo de 5
        type='video',
        order='date'
    ).execute()

    videos = search_response.get('items', [])

    # Filtramos videos para que busque el keyword solamente en el titulo del video
    videos_filtrados = [video for video in videos if texto.lower() in video['snippet']['title'].lower()]

    if not videos_filtrados:
        await interaction.followup.send(f"No encontré videos en YouTube con '{texto}' en el título", ephemeral=True)
        return

    # Armamos el embed para la respuesta de los videos de YouTube
    embedYouTube = discord.Embed(
        title=f"Videos subidos a nuestro canal",
        color=discord.Color.blue()
    )

    for video in videos_filtrados:
        title = video['snippet']['title']
        video_id = video['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_url = video_url[:15] + '\u200B' + video_url[15:]  # Anti-embed truncation trick
        embedYouTube.add_field(name=title, value=video_url, inline=False)
    
    # Mandamos la respuesta
    await interaction.followup.send(embed=embedYouTube, ephemeral=True)

    # Log
    print(FechaActual)
    print(f"Se ha ejecutado el comando /nerdearla para '{texto}'")

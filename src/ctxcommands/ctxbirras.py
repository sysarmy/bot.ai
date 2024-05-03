from datetime import datetime, timezone
import requests
from ics import Calendar
import re

async def birrasfunctx(ctx):
    FechaActual = datetime.now(timezone.utc)

    # Fetch the URL of the public calendar
    response = requests.get("https://calendar.google.com/calendar/u/0/ical/c_ntsrg10qsjmfeshhgap8ane1ss%40group.calendar.google.com/public/basic.ics")
    calendar = Calendar(response.text)

    eventosformateados = ""
    for event in calendar.events:
        # Convertimos las timezones para poder compararlas
        evento_UTC = event.begin.datetime.astimezone(timezone.utc)

        if evento_UTC > FechaActual:
            
            # Formateo de fecha
            fechaformateada = evento_UTC.strftime("%d-%m-%Y %H:%M")

            # Limpiamos el codigo feo que mete Google Calendar + sacamos la referencia del adminbirrator
            description = re.sub(r'<a href=\'(.*?)\'>.*?</a>', r'\1', event.description)
            description = re.sub(r'^Evento creado por https://github.com/sysarmy/disneyland/tree/master/adminbirrator 🍻$', '', description, flags=re.MULTILINE)

            evento = f"**Nombre:** {event.name}\n**Cuando:** {fechaformateada}\n**Descripcion:** {description}\n\n"
            eventosformateados += evento

    if eventosformateados:
        # Log + Mandamos mensaje
        print(FechaActual)
        print("Se ha ejecutado el comando !birras")

        await ctx.send(eventosformateados)
    else:
        # Log = Mandamos mensaje
        print(FechaActual)
        print("Se ha ejecutado el comando !birras")
        await ctx.send("No hay birras o eventos programados proximamente. Revisa: https://www.meetup.com/sysarmy/")
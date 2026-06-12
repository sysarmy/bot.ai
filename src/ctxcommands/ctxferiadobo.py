import requests
import discord
import datetime
import json
from ratelimit import limits

quince_minutos = 900

# Limitamos las API calls por las dudas. Esta libreria es medio negra. Lo dejamos asi por ahora, Mariano del futuro lo va a hacer manual
@limits(calls=15, period=quince_minutos)
async def feriadobofunctx(ctx):
    today = datetime.date.today()
    anio = datetime.date.today().year
    
    # Llama a la API
    response = requests.get(f"https://date.nager.at/api/v3/PublicHolidays/{anio}/BO")
    try:
        if response.status_code == 200:
            
            # Carga el JSON en Python dictionaro
            json_feriado = json.loads(response.text)          
            feriadosAR = response.json()
            dicferiados = []
            
            for dia in feriadosAR:
                nombre = dia["localName"]
                fecha_str = dia["date"]
                fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date() #Convierte fecha para poder chequearla con la fecha de hoy
                feriado = {"nombre": nombre, "fecha": fecha}
                dicferiados.append(feriado)
            
            # Compara fecha de los feriados con la actual para devolver solo las fechas que se vienen
            proximos_feriados = [feriado for feriado in dicferiados if feriado['fecha'] >= today] 

            # Log
            FechaActual = datetime.datetime.now()
            print(FechaActual)
            print(f"Comando FeriadoBO ejecutado")
            
            # Se crea el mensaje con los feriados
            message = "Próximos feriados en Bolivia:\n"
            
            for feriado in proximos_feriados[:3]:
                message += f"{feriado['fecha']} - {feriado['nombre']}\n"

            await ctx.send(message)

        else:
            print(f"Error: {response.status_code}. Pincho la API.")
            print(f"Error en la API {response.status_code}")
            
            # En caso de error en la API, se imprime el mensaje
            await ctx.send('Error en la API. Por favor avisar a algun root')
    
    except Exception as e:
        print(f"Error en la API: {e}")

    
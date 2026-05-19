import discord
from datetime import datetime
from discord.ext import commands



async def holamundofunctx(ctx, texto):
    FechaActual = datetime.now()
    
    mensajebienvenida = """Bienvenido a la comunidad. Acá tenés un resumen de los canales disponibles en IRC de Sysarmy:
        #sysarmy-gaming: Este canal es para discutir de gaming y llamar al call to action respecto a tetr.io sin inundar #sysarmy con la pasión del apilado de bloques.
        #sysarmy-help: Este canal tiene el RSS de help.sysarmy.com y ademas se puede usar para preguntas.
        #sysarmy-memes: Este canal es solo para postear memes.
        #sysarmy-offtopic: El canal donde sgoico y nachi pasan productos 4 o 5 octogonos a probar.
        #sysarmy-timba: No tomes nada de lo que se diga aquí como un consejo financiero. Asesorate con profesionales y hacé tu propia investigación.
        #sysarmy-yelling: UNA MANERA MUY SATISFACTORIA DE EXPRESAR TU FRUSTRACIÓN Y UNA GRAN LECTURA PARA LOS DEMÁS TAMBIÉN.  SOLO CAPS/MAYÚSCULAS.
                      Mas detalles en el canal #help-bot-commands de Discord, dentro de la seccion de Welcome! - o ejecutando /help desde Discord"""
    await ctx.send(mensajebienvenida)

    # Log
    print(FechaActual)
    print (f'Se ha ejecutado el comando !holamundo')
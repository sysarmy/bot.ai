import discord
from datetime import datetime
from discord.ext import commands



async def helpfunctx(ctx, texto):
    FechaActual = datetime.now()
    
    if texto is None:
        
        mensajeayuda_general = """Informacion general sobre los comandos del bot de Sysarmy       
              !dolar !cripto !euro !fulbo !pesos !clima !subte !underground !feriadoar !feriadocl !feriadoes !feriadomx !feriadouy !q !qsearch !qadd !rank !kgivers !kgiven !karma !birras !flip !shrug !nerdearla !jobs !f1 !mundial
                          Mas detalles en el canal #help-bot-commands de Discord, dentro de la seccion de Welcome! - o ejecutando /help desde Discord"""
        await ctx.send(mensajeayuda_general)
   
    elif texto == "clima":
        mensajeayuda_clima = """clima en Discord o !clima para usuarios externos. Devuelve el clima en base a la ciudad de input. Ej: '!clima London'. 
                                Recordar poner bien el input de la ciudad. Tener en cuenta que algunas ciudades pueden llevar el nombre en ingles (por ejemplo, London)
                            """
        await ctx.send(mensajeayuda_clima)
    elif texto == "karma":
        mensajeayuda_karma = """/karma en Discord o !karma para usuarios externos. Devuelve el karma de la palabra o usuario que se inserte. Ej: '!karma ubuntu'. Para dar karma
                                usar ++ o -- en cada palabra o usuario. Ej: 'ubuntu--' o jedux++'
                            """
        await ctx.send(mensajeayuda_karma)
    elif texto == "fulbo":
        mensajeayuda_fulbo = """fulbo en Discord o !fulbo para usuarios externos. Devuelve los resultados de la ultima fecha de la liga seleccionada ('!fulbo BL1'). 
                                Ligas disponibles ==> PL = Premiere League, BL1 = Bundesliga, PD = La Liga España, FL1 = Liga Francia, SA = Serie A Italia
                            """
        await ctx.send(mensajeayuda_fulbo)
    elif texto == "qadd":
        mensajeayuda_qadd = """Agrega todo el texto insertado despues del comando. EL_FORMATO IS DEFINED AS: <@supreme_leader> because I say so. | <peasant1> yes m'Lord. 
                                | <peasant2> it wont happen again, Sire. | <peasant-n> please forgive us.
                            """
        await ctx.send(mensajeayuda_qadd)

    elif texto == "cripto":
        await ctx.send("Pone !cripto y te da los precios de la timba. No requiere argumentos")

    elif texto == "dolar":
        await ctx.send("Pone !dolar y te da los precios de la timba. Opcionalmente se puede especifica el valor en pesos, Ej: '!dolar 500'")

    elif texto in ["feriado", "feriadoar", "feriadomx", "feriadoes", "feriadocl", "feriadouy"]:
      await ctx.send("Pone !feriadouy !feriadoar !feriadocl !feriadoes !feriadomx y te da los proximos feriados para el pais seleccionado. No requiere argumentos")   

    elif texto == "euro":
      await ctx.send("Pone !euro y te da los precios de la timba. No requiere argumentos")
    
    elif texto == "subte":
      await ctx.send("Pone !subte y te da el estado del subte en Buenos Aires. No requiere argumentos")

    elif texto == "underground":
      await ctx.send("Pone !underground y te da el estado del subte en Londres. No requiere argumentos")

    elif texto == "underground":
      await ctx.send("Pone !underground y te da el estado del subte en Londres. No requiere argumentos")

    elif texto == "pesos":
      await ctx.send("Pone !pesos y el monto para que te calcule el precio en USD. Ej: '!pesos 10000'")

    elif texto == "birras":
      await ctx.send("Pone !birras para consultar las proximas Adminbirras en el Google Calendar publico de Sysarmy. No requiere argumentos")

    elif texto == "nerdearla":
      await ctx.send("Pone !nerdearla para consultar charlas subidas a YouTube y agenda de Nerdearla en base a un texto. Ej: '!nerdearla kubernetes'")

    elif texto == "jobs":
      await ctx.send("Pone !jobs para consultar trabajos posteados por recruiters en nuestro canal de jobs. Ej: '!jobs backend'")

    elif texto == "f1":
       await ctx.send("'!f1 carrera' devuelve resultados del ultimo GP  ||  '!f1 temporada' las posiciones generales")

    elif texto == "mundial":
       await ctx.send("Pone !mundial para consultar los partidos del dia de la Copa del Mundo FIFA 2026. No requiere argumentos")

    # Log
    print(FechaActual)
    print (f'Se ha ejecutado el comando !help para {texto}')
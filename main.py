# IMPORT DE LIBRERIAS PRINCIPALES
import discord
from discord import Intents, Client, Message, app_commands, Interaction, Embed, message, reaction
from discord.ext import commands
import random, sqlite3
from datetime import datetime, timedelta, timezone
from db.dbops import agregarusuario, sincronizarUsuarios
import os
from dotenv import load_dotenv
import re

# IMPORT DE COMANDOS TREE (NATIVOS DISCORD)
from src.londonUnderground import Lines
from src.subteBA import SubteBA
from src.fulbo import futbolimport
from src.Clima import climafun
from src.cripto import criptofun
from src.caucho import cauchofun
from src.dolar import dolarfun
from src.euro import eurofun
from src.pesos import pesosfunc
from src.tasa import tasafun
from src.feriadoAR import feriadoARfun
from src.feriadoCL import feriadoCLfun
from src.feriadoES import feriadoESfun
from src.feriadoMX import feriadoMXfun
from src.feriadoUY import feriadoUYfun
from src.birras import birrasfunc
from src.karma import karmagiversfunc, karmarankfunc, karmauserfunc
from src.help import helpfunc
from src.quote import quotefunc, qsearchfunc
from src.nerdearla import nerdearlacharlasfunc
from src.shithappens import ShitHappens
from src.f1 import f1func

#IMPORT DE FUNCIONES PARA SISTEMA DE JOBS
from src.jobsearch import jobsearchfunc
from src.discordjobs.postjob_native import JobPostModal
from src.discordjobs.postjob_bulk import bulkjobpost
from src.discordjobs.postjob_gform_convert import checkforjobs
from src.discordjobs.postjob_gform import gformjobpost
from src.tasks import scheduled_job_posting, scheduled_bulk_job_posting

# IMPORT DE COMANDOS VERSION SIMPLE (FUNCIONAN POR TEXTO USANDO FUNCION CTX.SEND) 
from src.ctxcommands.ctxclima import climafunctx
from src.ctxcommands.ctxcripto import criptofunctx
from src.ctxcommands.ctxcaucho import cauchofunctx
from src.ctxcommands.ctxdolar import dolarfunctx
from src.ctxcommands.ctxeuro import eurofunctx
from src.ctxcommands.ctxpesos import pesosfunctx
from src.ctxcommands.ctxferiadoar import feriadoarfunctx
from src.ctxcommands.ctxferiadocl import feriadoclfunctx
from src.ctxcommands.ctxferiadomx import feriadomxfunctx
from src.ctxcommands.ctxferiadouy import feriadouyfunctx
from src.ctxcommands.ctxferiadoes import feriadoesfunctx
from src.ctxcommands.ctxbirras import birrasfunctx
from src.ctxcommands.ctxfulbo import fulbofunctx
from src.ctxcommands.ctxhelp import helpfunctx
from src.ctxcommands.ctxkarma import karmarankfunctx, karmawordfunctx, karmagiversfunctx, karmagiversuserfunctx
from src.ctxcommands.ctxquote import quotefunctx, qsearchfunctx, quoteaddfunctx
from src.ctxcommands.ctxsubte import subtefunctx
from src.ctxcommands.ctxunderground import undergroundfunctx
from src.ctxcommands.ctxnerdearla import nerdearlafunctx
from src.ctxcommands.ctxjobsearch import jobsearchfunctx
from src.ctxcommands.ctxf1 import formula1ctxfunc
                                                                 

# BOFH - Discord community bot for Sysarmy
# Version 2.1 - Feb 2025
# by @Qwuor01 and @aragunde
# License GPL v2 - Ver LICENSE en repositorio                       
###########################################################################################################
########################### BOT INITIAL SETUP BEGINS ######################################################

load_dotenv()
monitoring_task = None # Para Discord Jobs

# Definimos a bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
BOT_token = os.getenv('BOT_token')

#Definicion de prefix, para buscarlo en cualquier parte del mensaje
def get_prefix(bot, message):
    prefixes = ['!']
    for prefix in prefixes:
        if prefix in message.content:
            return prefix
    # Default prefix
    return '!'

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

# FUNCION PRINCIPAL PARA ARRANCAR EL BOT 
def main() -> None:
    bot.run(f'{BOT_token}')

################## FETCHING DE USUARIOS A LA DB CUANDO SE UNEN AL SERVER

@bot.event
async def on_member_join(member):
    
    # Traemos el nombre y ID del usuario
    username = member.name
    user_id = str(member.id)

    # Mensaje de Bienvenida privado al usuario
    await member.send("Welcome to Sysarmy. Por favor recorda pasar por la seccion de Welcome para familiarizarte con el codigo de conducta y comandos de nuestro bot. Have fun :)")
    
    # Mandamos la data a la funcion de DB Ops que la agrega a la base
    await agregarusuario(username, user_id)


@bot.event
async def on_ready():

    # Trae todos los usuarios presentes en el server y lost agrega a la DB - Corre por unica vez cuando se inicia el bot
    # Esto lo hacemos para poder sincronizar el karma ranking y karmagiven de Discord desde nuestra DB
    guild_id = os.getenv('guild_id')
    guild = bot.get_guild(int(guild_id))
    all_members = guild.members
    await sincronizarUsuarios(all_members)

    try:
        scheduled_job_posting.start(bot)
        scheduled_bulk_job_posting.start(bot)
        print("Tareas programadas iniciadas")
    except Exception as e:
        print(f"Error al iniciar tareas programadas: {e}")
        pass

    # BOFH starts
    FechaActual = datetime.now()
    print("Current time:", FechaActual)
    print("""
               ...........     ..  ...  ..     ............     
              @@@@@@@@@@@@    @@@     @@@@    @@@@@@@@@@@@   
             @@@@            @@@@    .@@@    %@@@            
             @@@@@@@@@@@@    @@@@@@@@@@@@    @@@@@@@@@@@@    
            @@@@@@@@@@@@    @@@@@@@@@@@@    #@@@@@@@@@@@.    
            %%%%%%%%@@@@    %%%%%%%%@@@@    %%%%%%%%@@@@     
           @@@@@@@@@@@@.   @@@@@@@@@@@@    %@@@@@@@@@@@:     
                                                             
                                                             
          @@@@@@@@@@@@    @@@@@@@@@@@@    @@@@@@@@@@@@       
         @@@@@@@@@@@@.   @@@@@@@@@@@@    #@@@@@@@@@@@:       
         @@@:    @@@@    @@@     .@@@    @@@@@@@@@@@@        
        @@@@@@@@@@@@.   @@@: @@@@@@@.   %@@@@@@@@@@@:        
        @@@@@@@@@@@@    @@@ +@@#        @@@@@@@@@@@@         
       %@@@     @@@.   @@@: @@@@@@@    #@@@@@@@@@@@:         
       @@@+    @@@@    @@@ +@@@@@@@    @@@@@@@@@@@@          
                                                             
                                                             
     #@@@@@@@@@@@.   @@@@@@@@@@@@    *@@@     @@@:           
     @@@@@@@@@@@@    @@@@@@@@@@@@    @@@+    @@@@            
    @@@@@@@@@@@@:   @@@  @@@ %@@.   #@@@@@@@@@@@=            
    @@@@@@@@@@@@    @@@ @@@. @@@    @@@@@@@@@@@@             
   #@@@@@@@@@@@.   @@@  @@@ #@@             @@@:             
   @@@@@@@@@@@@    @@@ %@@. @@@    @@@@@@@@@@@@              
   ...........     ..  ...  ..     ............     
          
          BOFH bot is ready to pwn!""") 

    try:
        synced = await bot.tree.sync()
        print(f"Se sincronizaron {len(synced)} comandos slash")
    except Exception as e:
        print(e)


################ FUNCION DE RSS PARA EL CANAL DE SHITHAPPENS ################
    shitChannel = int(os.getenv('shitChannel'))
    channel = bot.get_channel(shitChannel)

    if isinstance(channel, discord.TextChannel):
        ShitHappens(channel, bot)
    else:
        print("Error: El canal no es el indicado")


########################### BOT INITIAL SETUP ENDS ######################################################
#########################################################################################################

##################################################################################################################
############################# FUNCION DE ON_REACTION PARA KARMA Y QUOTES #########################################
##################################################################################################################

# Operaciones para cuando una reaccion de Discord se agrega (Para Karma y quote)

@bot.event
async def on_reaction_add(reaction, user):
    FechaActual = datetime.now()

    # Conectamos a la base
    database = sqlite3.connect('db/discordusrs.db')
    databasequotes = sqlite3.connect('db/quotes.db')
    cursor = database.cursor()
    cursorquotes = databasequotes.cursor()

    # Esto hace que el usuario no pueda autoquotearse o darse/quitarse karma a si mismo
    if user != reaction.message.author:

        # Reaccion de Karma Up
        if "kup" in str(reaction):
            print(FechaActual)
            print("Karma +1")
            SQLkarma = ("UPDATE usuarios SET karma = karma + 1 WHERE user_id = ?")
            cursor.execute(SQLkarma, (reaction.message.author.id,))
            # Operaciones de DB
            SQLkarmagiven = ("UPDATE usuarios SET karmagiven = karmagiven + 1 WHERE user_id = ?")
            cursor.execute(SQLkarmagiven, (user.id,))
            mensaje = f"+1 karma para {str(reaction.message.author.display_name)} \n"
            mensaje += f"+1 karmagiven para {user.name}"
            await reaction.message.channel.send(mensaje)

        # Reaccion de Karma Down
        elif "kdown" in str(reaction):
            print("Karma -1")
            SQLkarma = ("UPDATE usuarios SET karma = karma - 1 WHERE user_id = ?")
            cursor.execute(SQLkarma, (reaction.message.author.id,))
            # Operaciones de DB
            SQLkarmagiven = ("UPDATE usuarios SET karmagiven = karmagiven + 1 WHERE user_id = ?")
            cursor.execute(SQLkarmagiven, (user.id,))
            await reaction.message.channel.send(f"-1 karma para {str(reaction.message.author.display_name)}")

    # Reaccion de Quote y agrega quote a la DB
    if "qadd" in str(reaction):
        SQLbuscar = ("SELECT quote FROM quotes WHERE quote = ? AND username = ?")
        cursorquotes.execute(SQLbuscar, (str(reaction.message.content), str(reaction.message.author)))
        quotesencontradas = cursorquotes.fetchall()
        if len(quotesencontradas) == 0:
            print(len(quotesencontradas))
            print("Mensaje quoteado")
            print(f"Message: {reaction.message.content}")
            print(f"Author: {reaction.message.author}")
            print(f"Date: {reaction.message.created_at}")
            SQLquote = ("INSERT INTO quotes (quote, username, date) VALUES (?, ?, ?)")
            cursorquotes.execute(SQLquote, (str(reaction.message.content), str(reaction.message.author), str(reaction.message.created_at)))
            await reaction.message.channel.send(f"Quote de {str(reaction.message.author.display_name)} agregado: {str(reaction.message.content)} - cortesia de: {str(user)}")
        else:
            await user.send("Error de capa 8. Este quote ya fue agregado anteriormente")
        
    database.commit()
    database.close()
    databasequotes.commit()
    databasequotes.close()

# Operaciones para cuando una reaccion de Discord se remueve (Para Karma y quote)

@bot.event
async def on_reaction_remove(reaction, user):
    FechaActual = datetime.now()

    # Conectamos a la base
    database = sqlite3.connect('db/discordusrs.db')
    databasequotes = sqlite3.connect('db/quotes.db')
    cursor = database.cursor()
    cursorquotes = databasequotes.cursor()
    
    # Esto hace que el usuario no pueda autoquotearse o darse/quitarse karma a si mismo
    if user != reaction.message.author:

        # Reaccion de Karma Up
        if "kup" in str(reaction):
            print(FechaActual)
            print("kup reaction removida")
            print("Karma -1")
            SQLkarma = ("UPDATE usuarios SET karma = karma - 1 WHERE user_id = ?")

            # Operaciones de DB
            cursor.execute(SQLkarma, (reaction.message.author.id,))
            SQLkarmagiven = ("UPDATE usuarios SET karmagiven = karmagiven - 1 WHERE user_id = ?")
            cursor.execute(SQLkarmagiven, (user.id,))
            await reaction.message.channel.send(f"karma++ removido para {str(reaction.message.author.display_name)}")
        
        # Reaccion de Karma Down
        elif "kdown" in str(reaction):
            print(FechaActual)
            print("kdown reaction removida")
            print("Karma +1")
            SQLkarma = ("UPDATE usuarios SET karma = karma + 1 WHERE user_id = ?")

            # Operaciones de DB
            cursor.execute(SQLkarma, (reaction.message.author.id,))
            SQLkarmagiven = ("UPDATE usuarios SET karmagiven = karmagiven - 1 WHERE user_id = ?")
            cursor.execute(SQLkarmagiven, (user.id,))
            await reaction.message.channel.send(f"karma-- removido para {str(reaction.message.author)}")

        # Reaccion de Quote y remueve quote de la DB
        elif "qadd" in str(reaction):
            print("Quote removido")
            print(f"Message: {reaction.message.content}")
            print(f"Author: {reaction.message.author}")
            print(f"Date: {reaction.message.created_at}")
            SQLquote = ("DELETE FROM quotes WHERE quote = ? AND username = ?")
            cursorquotes.execute(SQLquote, (str(reaction.message.content), str(reaction.message.author)))
            await reaction.message.channel.send(f"Quote de {str(reaction.message.author)} removido")

    database.commit()
    database.close()
    databasequotes.commit()
    databasequotes.close()

################### MANEJO DE ERRORES Y SETUP DE ON_MESSAGE ###################

# Funcion de manejo de error cuando el argumento es None
# (usuario manda el comando sin parametros requeridos, como por ejemplo en !clima o !fulbo)
# Excepto para !help que tiene su propio mensaje si el comando va vacio

@bot.event
async def on_command_error(ctx, error):
    FechaActual = datetime.now()

    mensajeayuda_general = """Informacion general sobre los comandos del bot de Sysarmy       
                        !dolar !caucho !cripto !euro !pesos !tasa !fulbo !clima !subte !underground !feriadoar !feriadocl !feriadoes !feriadomx !feriadouy !q !qsearch !qadd !rank !kgivers !kgiven !karma !nerdearla !jobs !f1
                        Mas detalles en el canal #help-bot-commands de Discord, dentro de la seccion de Welcome! - o ejecutando /help desde Discord"""

# Custom error handling - si !help se manda vacio sin especificar comando, manda un mensaje de ayuda general
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.name == "help":
            await ctx.send(mensajeayuda_general)

            # Log
            print(FechaActual)
            print ("Se ha ejecutado el comando !help")
        
        elif ctx.command.name == "caucho":
            await cauchofunctx(ctx, None)
            # Log
            print(FechaActual)
            print ("Se ha ejecutado el comando !caucho")
          
        elif ctx.command.name == "dolar":
            await dolarfunctx(ctx, None)
            # Log
            print(FechaActual)
            print ("Se ha ejecutado el comando !dolar")

        elif ctx.command.name == "f1":
            await ctx.send("No pasaste argumentos. Usa `!f1 temporada` o `!f1 carrera`.")
            # Log
            print(FechaActual)
            print ("Se ha ejecutado el comando !f1")

        else:
            await ctx.send("Error en el comando. No pasaste argumentos.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando inexistente")
    else:
        await ctx.send("Error en el comando. No pasaste argumentos.")


##################################################################################################################
############################# FUNCION DE ON_MESSAGE PARA KARMA ++ y -- ###########################################
##################################################################################################################
@bot.event
async def on_message(message):
    FechaActual = datetime.now()

    # Conectamos a la base de karma
    databasekarma = sqlite3.connect('db/karma.db')
    cursorkarma = databasekarma.cursor()
    databaseusers = sqlite3.connect('db/discordusrs.db')
    cursorusers = databaseusers.cursor()
    cursorupdateusers = databaseusers.cursor()    

    palabra_base = None

    BridgeBotID = os.getenv('bridgebotID') # <--- Aca va el usr ID del Bridge bot de Discord

    if message.author.bot and not str(message.author.id) == BridgeBotID:
        return
    else:
##################################################################################################################
# Todo esto se ejecuta cuando el usuario es el bot de bridge (o sea, el mensaje viene bridgeado de IRC, Slack, Telegram, etc.)

        if str(message.author.id) == BridgeBotID:

                # Funcion para encontrar el prefijo del comando en cualquier parte del mensaje (para cuando lo manda el bridge bot)
            if '> !' in message.content:
                # Extraemos el mensaje que viene despues del prefijo y cambiamos el mensaje original para pasarselo al bot y que ejecute el comando
                command_start = message.content.index('!')
                new_content = message.content[command_start:]
                
                message.content = new_content
                # de https://github.com/Rapptz/discord.py/issues/2238#issuecomment-504252776
                # esto es necesario para invocar los comandos directamente porque si sigue el codigo y entra por el process_comand 
                # tira return sin hacer nada porque bot=true esto es menos cerdo que sobreescribir el metodo.
                ctx = await bot.get_context(message)
                await bot.invoke(ctx)

            # Traemos el texto del mensaje y lo buscamos en la base
            textokarma = message.content.split()
            for texto in textokarma:
           #     if texto.endswith("++") or texto.endswith("--"):
                if re.match(r'^[a-zA-Z0-9ñÑáéíóú]+(\+\+|\-\-)$', texto): # Este regex es feo pero anda     
                    palabra_base = texto[:-2]

                    # Buscamos y traemos el username externo <--- Esto es asi porque el bot siempre empieza los mensajes con el usuario
                    # en este formato = "<usuarioexterno> Mensaje publicado al canal." 
                    start_index = message.content.find('<')
                    end_index = message.content.find('>')
                    IRCusername = message.content[start_index + 1:end_index]
                        
                    # Ejecuta query para verificar si la palabra existe en la DB
                    cursorkarma.execute("SELECT * FROM karma WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                    existing_word = cursorkarma.fetchone()

                    # Ejecuta query para verificar si el usuario existe en la DB
                    cursorkarma.execute("SELECT * FROM karma WHERE LOWER(palabra) = ? AND isuser = 'YES'", (IRCusername.lower(),))
                    existing_user = cursorkarma.fetchone()
                        
                    # Si la palabra existe, procede con las funciones de UPDATE
                    if existing_word:
                                
                            # Update word en la DB para karma++ y se imprime confirmacion
                            if texto.endswith("++"):
                                cursorkarma.execute("UPDATE karma SET karmavalue = karmavalue + 1 WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                                databasekarma.commit()
                                cursorkarma.execute("SELECT karmavalue FROM karma WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                                updated_karma = cursorkarma.fetchone()[0]
                                print(FechaActual)
                                print(f"Karma++ para {palabra_base}!")
                                mensaje = f"+1 karma para {palabra_base.lower()}. Current karma is: {updated_karma} \n"
                                
                                # Ahora Chequeamos el autor del mensaje
                                if existing_user:
                                    # Se le da karmagiven al usuario y se imprime confirmacion
                                    cursorkarma.execute("UPDATE karma SET karmagiven = karmagiven + 1 WHERE LOWER(palabra) = ? AND isuser = 'YES'", (IRCusername.lower(),))
                                    databasekarma.commit()
                                    print(f"+1 Karmagiven para {IRCusername}")
                                    mensaje += f"+1 karmagiven para <{IRCusername}>"
                                    await message.channel.send(mensaje)

                                elif existing_user is None:
                                    # Se agrega al nuevo usuario a la DB con karmagiven inicial y se imprime confirmacion
                                    cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, 1, 'YES', 0)", (IRCusername.lower(),))
                                    cursorkarma.execute("UPDATE karma SET karmagiven = karmagiven + 1 WHERE palabra = ? AND isuser = 'YES'", (IRCusername.lower(),))
                                    databasekarma.commit()
                                    cursorkarma.execute("SELECT palabra FROM karma WHERE LOWER(palabra) = ? AND isuser = 'YES'", (IRCusername.lower(),))
                                    print(f"Nuevo usuario externo [{IRCusername}] agregado a la DB!.")
                                    mensaje += f"+1 karmagiven para <{IRCusername}>. Welcome to the karma user list! "
                                    await message.channel.send(mensaje)
                            
                                # Update word en la DB para karma-- y se imprime confirmacion
                            elif texto.endswith("--"):
                                cursorkarma.execute("UPDATE karma SET karmavalue = karmavalue - 1 WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                                databasekarma.commit()
                                cursorkarma.execute("SELECT karmavalue FROM karma WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                                updated_karma = cursorkarma.fetchone()[0]
                                print(FechaActual)
                                print(f"Karma--  para {palabra_base}!")
                                await message.channel.send(f"-1 karma para {palabra_base.lower()}. Current karma = {updated_karma}")

                    # Si la palabra no existe, procede con las funciones de INSERT
                    else:
                        # Insert word en la DB para karma++ y se imprime confirmacion
                        if texto.endswith("++"):
                            initial_karma = 1 # <-- Como es una nueva palabra y es ++, el karma inicial siempe es de 1
                            cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, ?, 'NO', ?)", (palabra_base.lower(), initial_karma, 0))
                            databasekarma.commit()
                            cursorkarma.execute("SELECT karmavalue FROM karma WHERE palabra = ?", (palabra_base.lower(),))
                            updated_karma = cursorkarma.fetchone()[0]
                            print(f"Nueva palabra agregada a la DB. Karma++  para {palabra_base}")
                            mensaje = f"+1 karma para {palabra_base}. Current karma is: {updated_karma} \n"

                            # Chequeamos el autor del mensaje
                            if existing_user:
                                # Se le da karmagiven al usuario y se imprime confirmacion
                                cursorkarma.execute("UPDATE karma SET karmagiven = karmagiven + 1 WHERE LOWER(palabra) = ? AND isuser = 'YES'", (IRCusername.lower(),))
                                databasekarma.commit()
                                print(FechaActual)
                                print(f"Se ha dado karmagiven +1 a {IRCusername}.")
                                mensaje += f"+1 karmagiven para <{IRCusername}>."
                                await message.channel.send(mensaje)

                            elif existing_user is None:
                                # Se agrega al nuevo usuario a la DB con karmagiven inicial y se imprime confirmacion
                                cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, 1, 'YES', 0)", (IRCusername.lower(),))
                                cursorkarma.execute("UPDATE karma SET karmagiven = karmagiven + 1 WHERE palabra = ? AND isuser = 'YES'", (IRCusername.lower(),))
                                databasekarma.commit()
                                cursorkarma.execute("SELECT palabra FROM karma WHERE palabra = ? AND isuser = 'YES'", (IRCusername,))
                                print(f"Nuevo usuario externo [{IRCusername}] agregado a la DB!.")
                                mensaje += f"+1 karmagiven para <{IRCusername}>. Welcome to the karma user list!"
                                await message.channel.send(mensaje)
                        
                        # Insert palabra en la DB para karma-- y se imprime confirmacion
                        elif texto.endswith("--"):
                            initial_karma = -1 ## <-- Como es una nueva palabra y es --, el karma inicial siempe es de -1
                            cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, ?, 'NO', ?)", (palabra_base.lower(), initial_karma, 0))
                            databasekarma.commit()
                            cursorkarma.execute("SELECT karmavalue FROM karma WHERE palabra = ?", (palabra_base.lower(),))
                            updated_karma = cursorkarma.fetchone()[0]
                            print(FechaActual)
                            print(f"Nueva palabra agregada a la DB. Karma--  para {palabra_base}")
                            await message.channel.send(f"-1 karma para {palabra_base}. Current karma = {updated_karma}")

##################################################################################################################     
# Todo esto se ejecuta cuando el usuario NO es el bot (o sea, un usuario normal nativo de Discord)

        else:
            # Traemos el texto del mensaje y lo buscamos en la base
            textokarma = message.content.split()
            
            for texto in textokarma:
                #if texto.endswith("++") or texto.endswith("--"):
                if re.match(r'^[a-zA-Z0-9ñÑáéíóú]+(\+\+|\-\-)$', texto): # Este regex es feo pero anda
                    palabra_base = texto[:-2]

                    # Ejecuta query para verificar: si la palabra existe ||| Si el usuario existe || Si el usuario se cambio el nombre de Discord (en ese caso lo actualiza)
                    cursorusers.execute("SELECT * FROM usuarios WHERE username = ?", (message.author.name,))
                    cursorupdateusers.execute("UPDATE usuarios SET username = ? WHERE user_id = ? AND username != ?", (message.author.name, message.author.id, message.author.name))
                    cursorkarma.execute("SELECT * FROM karma WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                    existing_word = cursorkarma.fetchone()
                    

                    # Si la palabra existe, procede con las funciones de UPDATE
                    if existing_word:
                            print(f"encontre la palabra en la base de datos {palabra_base}")

                            # Update word en la DB para karma++
                            if texto.endswith("++"):
                                cursorkarma.execute("UPDATE karma SET karmavalue = karmavalue + 1 WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                                databasekarma.commit()
                                cursorkarma.execute("SELECT karmavalue FROM karma WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                                updated_karma = cursorkarma.fetchone()[0]
                                print(FechaActual)
                                print(f"Karma ++ para {palabra_base}")
                                mensaje = f"+1 karma para {palabra_base.lower()}. Current karma is: {updated_karma} \n"

                                # Se le da karmagiven al usuario y se imprime mensaje
                                cursorusers.execute("UPDATE usuarios SET karmagiven = karmagiven + 1 WHERE username = ?", (message.author.name,))
                                databaseusers.commit()
                                cursorusers.execute("SELECT karmagiven FROM usuarios WHERE username = ?", (message.author.name,))
                                updated_karmagivenusr = cursorusers.fetchone()[0]
                                print(f"Se ha dado karmagiven +1 a {message.author.name}.")
                                mensaje += f"+1 karmagiven para {message.author}. Current karmagiven is: {updated_karmagivenusr}"
                                await message.channel.send(mensaje)
                            
                            # Update palabra en la DB para karma--
                            elif texto.endswith("--"):
                                cursorkarma.execute("UPDATE karma SET karmavalue = karmavalue - 1 WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                                databasekarma.commit()
                                cursorkarma.execute("SELECT karmavalue FROM karma WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                                updated_karma = cursorkarma.fetchone()[0]
                                print(FechaActual)
                                print(f"Karma -- para {palabra_base}")
                                await message.channel.send(f"-1 karma para {palabra_base.lower()}. Current karma is: {updated_karma}")
        
                    # Si la palabra no existe, procede con las funciones de INSERT
                    else:
                        # Insert palabra en la DB para karma++
                        if texto.endswith("++"):
                            initial_karma = 1
                            cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, ?, 'NO', ?)", (palabra_base.lower(), initial_karma, 0))
                            databasekarma.commit()
                            cursorkarma.execute("SELECT karmavalue FROM karma WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                            updated_karma = cursorkarma.fetchone()[0]
                            print(FechaActual)
                            print(f"Nueva palabra agregada a la DB. Karma ++ para {palabra_base}")
                            mensaje = f"+1 karma para {palabra_base.lower()}. Current karma is: {updated_karma} \n"

                            # Se le da karmagiven al usuario y se imprime mensaje
                            cursorusers.execute("UPDATE usuarios SET karmagiven = karmagiven + 1 WHERE username = ?", (message.author.name,))
                            databaseusers.commit()
                            cursorusers.execute("SELECT karmagiven FROM usuarios WHERE username = ?", (message.author.name,))
                            updated_karmagivenusr = cursorusers.fetchone()[0]
                            print(f"Se ha dado karmagiven +1 a {message.author.name}.")
                            mensaje += f"+1 karmagiven para {message.author}. Current karmagiven is: {updated_karmagivenusr}"
                            await message.channel.send(mensaje)
                        
                        # Insert palabra en la DB para karma--
                        elif texto.endswith("--"):
                            initial_karma = -1
                            cursorkarma.execute("INSERT INTO karma (palabra, karmavalue, isuser, karmagiven) VALUES (?, ?, 'NO', ?)", (palabra_base.lower(), initial_karma, 0))
                            databasekarma.commit()
                            cursorkarma.execute("SELECT karmavalue FROM karma WHERE LOWER(palabra) = ?", (palabra_base.lower(),))
                            updated_karma = cursorkarma.fetchone()[0]
                            print(FechaActual)
                            print(f"Nueva palabra agregada a la DB. Karma -- para {palabra_base}")
                            await message.channel.send(f"-1 karma para {palabra_base.lower()}. Current karma is: {updated_karma}")


    databasekarma.commit()
    databasekarma.close()
    databaseusers.commit()
    databaseusers.close()

################### FUNCION DE ON_MESSAGE PARA YELLING ###################

#Lee el canal de Yelling
    if message.channel.id == 758773471315492925:
        # Checkea usuarios que vienen de IRC
        irc_relay_pattern = re.compile(r'^<[^>]+>\s*(.*)$')
        irc_match = irc_relay_pattern.match(message.content)

        # Si no es de IRC, chequea el mensaje a partir de <usuario>
        if irc_match:
            text_to_check = irc_match.group(1)
        else:
            text_to_check = message.content


        # Regex para URLs y emojis
        url_and_emoji_pattern = re.compile(r'http[s]?://\S+|:[^:]+:')
        # Regex para palabras en lowercase
        lowercase_pattern = re.compile(r'\b[a-z]+\b')
        # Ignora URLs y emojis
        text_without_urls_and_emojis = url_and_emoji_pattern.sub('__IGNORED__', text_to_check)
        # Check for any lowercase words
        has_lowercase = lowercase_pattern.search(text_without_urls_and_emojis) is not None

#Chequeea por lowercase. Putea solo con haber un solo caracter en lowercase. No jodan.
        if has_lowercase: 
            print(FechaActual)
            print("Mensaje en lower case detectado en canal. Se ejecutara funcion de Yelling")

#Agarra frases random de un txt y las manda en respuesta al mensaje (para mas humillacion)
            with open("src/rtasyelling.txt", "r", encoding="utf8") as file: 
                lines = file.readlines()
            await message.reply(random.choice(lines).strip())

# Fin de todo, se va el mensaje a ser procesado por los comandos.         
    await bot.process_commands(message) # <-- No tocar esto jamas o rompe los comandos on_message. Siempre dejar al final de la funcion on_message

#########################################################################################
################### LLAMADAS DE COMANDOS TEXT BASED (USA FUNCION CTX) ###################

# Comandos indivuduales estan en .src/ctxcommands

# COMANDO HELP
@bot.command()
async def help(ctx, texto):
    await helpfunctx(ctx, texto)

# COMANDO CLIMA   
@bot.command()
async def clima(ctx, ciudad):
    await climafunctx(ctx, ciudad)

# COMANDO CRIPTO
@bot.command()
async def cripto(ctx):
    await criptofunctx(ctx)

# COMANDO FULBO
@bot.command()
async def fulbo(ctx, liga):
    await fulbofunctx(ctx, liga)   

# COMANDO CAUCHO
@bot.command()
async def caucho(ctx, monto):
    await cauchofunctx(ctx, monto)

# COMANDO DOLAR
@bot.command()
async def dolar(ctx, inputpesos):
    await dolarfunctx(ctx, inputpesos)

# COMANDO PESOS
@bot.command()
async def pesos(ctx, monto:int):
    await pesosfunctx(ctx, monto)

# COMANDO FERIADOS
@bot.command()
async def feriadoar(ctx):
    await feriadoarfunctx(ctx)

@bot.command()
async def feriadoes(ctx):
    await feriadoesfunctx(ctx)

@bot.command()
async def feriadocl(ctx):
    await feriadoclfunctx(ctx)

@bot.command()
async def feriadouy(ctx):
    await feriadouyfunctx(ctx)    

@bot.command()
async def feriadomx(ctx):
    await feriadomxfunctx(ctx)   

# COMANDO SUBTE
@bot.command()
async def subte(ctx):
    await subtefunctx(ctx)       

# COMANDO UNDERGROUND
@bot.command()
async def underground(ctx):
    await undergroundfunctx(ctx)

# COMANDO EURO       
@bot.command()
async def euro(ctx):
    await eurofunctx(ctx)   

# COMANDO KARMA RANK
@bot.command()
async def rank(ctx):
    await karmarankfunctx(ctx)

# COMANDO KARMA PALABRA
@bot.command()
async def karma(ctx, text):
    await karmawordfunctx(ctx, text)

# COMANDO RANK GIVERS              
@bot.command()
async def kgivers(ctx):
    await karmagiversfunctx(ctx)

# COMANDO KARMA GIVERS POR USUARIO            
@bot.command()
async def kgiven(ctx, text):
    await karmagiversuserfunctx(ctx, text)

# COMANDO QUOTE ADD
@bot.command()
async def qadd(ctx, *, quote: str):
    await quoteaddfunctx(ctx, quote)

# COMANDO QUOTE RANDOM
@bot.command()
async def q(ctx):
    await quotefunctx(ctx)

# COMANDO QUOTE SEARCH
@bot.command()
async def qsearch(ctx, texto):
    await qsearchfunctx(ctx, texto)

# COMANDO BIRRAS
@bot.command()
async def birras(ctx):
    await birrasfunctx(ctx)

# COMANDO PING
@bot.command()
async def ping(ctx):
    print(f"Se ha ejecutado el comando !ping")
    await ctx.send("Pong!")

# COMANDO FLIP
@bot.command()
async def flip(ctx):
    print(f"Se ha ejecutado el comando !flip")
    await ctx.send("(╯°□°）╯︵ ┻━┻")

# COMANDO SHRUG
@bot.command()
async def shrug(ctx):
    print(f"Se ha ejecutado el comando !flip")
    await ctx.send("¯\\_(ツ)_/¯")

# COMANDO NERDEARLA
@bot.command()
async def nerdearla(ctx, texto):
    await nerdearlafunctx(ctx, texto)

# COMANDO JOB SEARCH
@bot.command(name="jobs")
async def jobs(ctx, texto):
    await jobsearchfunctx(ctx, texto)

# COMANDO F1
@bot.command()
async def f1(ctx, texto):
    await formula1ctxfunc(ctx, texto)

#########################################################################################
################### LLAMADAS DE COMANDOS SLASH NATIVOS DISCORD (TREE) ###################

# Comandos individuales estan en .src

# COMANDO DOLAR
@bot.tree.command(name="preciodolar", description="Cotizacion del dolar")
async def preciodolar(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await dolarfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /dolar: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO CAUCHO
@bot.tree.command(name="tasacaucho", description="Tasas de caución")
async def tasacaucho(interaction: Interaction):
    try:
        await cauchofun(interaction)
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /tasacaucho: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO EURO
@bot.tree.command(name="precioeuro", description="Cotizacion del Euro")
async def precioeuro(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await eurofun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /euro: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO PESOS
@bot.tree.command(name="pesos", description="Calcula pesos a dolares")
async def pesosausd(interaction: Interaction, monto:int):
    try:
        await interaction.response.send_message(embed= await pesosfunc(interaction, monto))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /pesos: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO TASA
@bot.tree.command(name="tasa", description="Calcula rendimiento en pesos de varias tasas de caución")
async def rendimientocaucho(interaction: Interaction, monto:int):
    try:
        await interaction.response.send_message(embed= await tasafunc(interaction, monto))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /tasa: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO CLIMA
@bot.tree.command(name="clima", description="Información del clima")
async def Clima(interaction: Interaction, city:str):
    try:
        await interaction.response.send_message(embed=await climafun(interaction, city))  
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /clima: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO LONDON UNDERGROUND
@bot.tree.command(name="underground", description="Información del London Underground")
async def londonunderground(interaction: Interaction):
    try:
        await interaction.response.send_message(embed=Lines())
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /underground: Limite de API calls excedido. Sori el CTO no nos dio budget.")
    
# COMANDO HELP
@bot.tree.command(name="help", description="Como usar el bot")
async def ayudatree(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await helpfunc(interaction), ephemeral=True)
    except:
        pass

# COMANDO SUBTE
@bot.tree.command(name="subtebsas", description="Información de los Subtes")
async def subtebsas(interaction: Interaction):
    try:
        await interaction.response.send_message(embed=await SubteBA(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /subte: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO FULBO
@bot.tree.command(name="fulbo", description="Ultimos resultados de ligas de futbol")
async def futlbol(interaction: Interaction):
    try:
        await interaction.response.send_message(embed=await futbolimport(interaction))
    except:
        pass

# COMANDO CRIPTO
@bot.tree.command(name="cripto", description="Precio de criptomonedas")
async def preciocripto(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await criptofun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /cripto: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO FERIADO ARGENTINA
@bot.tree.command(name="feriadoar", description="Proximos feriados en Argentina")
async def feriadosar(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await feriadoARfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /feriadoar: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO FERIADO URUGUAY
@bot.tree.command(name="feriadouy", description="Proximos feriados en Uruguay")
async def feriadosuy(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await feriadoUYfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /feriadoar: Limite de API calls excedido. Sori el CTO no nos dio budget.")
    
# COMANDO FERIADO CHILE
@bot.tree.command(name="feriadocl", description="Proximos feriados en Chile")
async def feriadoscl(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await feriadoCLfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /feriadoar: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO FERIADO ESPAÑA
@bot.tree.command(name="feriadoes", description="Proximos feriados en España")
async def feriadoses(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await feriadoESfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /feriadoar: Limite de API calls excedido. Sori el CTO no nos dio budget.")

# COMANDO FERIADO MEXICO
@bot.tree.command(name="feriadomx", description="Proximos feriados en Mexico")
async def feriadosmx(interaction: Interaction):
    try:
        await interaction.response.send_message(embed= await feriadoMXfun(interaction))
    except:
        print(f"Limite de API calls excedido. Ultimo call hecho por {interaction.user}")
        await interaction.response.send_message("Comando /feriadoar: Limite de API calls excedido. Sori el CTO no nos dio budget.")
    
# COMANDO KARMA RANK
@bot.tree.command(name="karmarank", description="Ranking top 10 usuarios")
async def karmarank(interaction: Interaction):
    await interaction.response.send_message(embed = await karmarankfunc(interaction))

# COMANDO KARMA GIVERS
@bot.tree.command(name="karmagivers", description="Ranking top 5 dadores de karma")
async def karmagivers(interaction: Interaction):
    # Manda el primer embed con givers de discord
    embed_discord, embed_karma = await karmagiversfunc(interaction)
    await interaction.response.send_message(embed=embed_discord)
    
    # Manda el segundo embed con givers externos
    await interaction.followup.send(embed=embed_karma)

# COMANDO KARMA USER
@bot.tree.command(name="karmauser", description="Ver Karma de un usuario")
async def karmauser(interaction: Interaction, member: discord.Member):
    await interaction.response.send_message(embed= await karmauserfunc(interaction, member))

# COMANDO QUOTE RANDOM
@bot.tree.command(name="quote", description="Devuelve un quote random del hisotrial")
async def quoterandom(interaction: Interaction):
    await interaction.response.send_message(embed= await quotefunc(interaction))

# COMANDO QUOTE SEARCH
@bot.tree.command(name="qsearch", description="Busca un Quote en base a texto")
async def quotesearch(interaction: Interaction, texto:str):
    await interaction.response.send_message(embed= await qsearchfunc(interaction, texto))

# COMANDO BIRRAS
@bot.tree.command(name="birrassysarmy", description="Proximas birras / eventos de Sysarmy")
async def birras(interaction: Interaction):
    await interaction.response.send_message(embed= await birrasfunc(interaction))

# COMANDO NERDEARLA
@bot.tree.command(name="nerdearlacharlas", description="Busca charlas de Nerdearla en YouTube y agenda de evento")
async def nerdearlacharlas(interaction: Interaction, texto:str):
    await nerdearlacharlasfunc(interaction, texto)

# COMANDO JOB SEARCH
@bot.tree.command(name="jobsearch", description="Busca posiciones posteadas por recruiters en nuestro canal de jobs")
async def jobsearch(interaction: discord.Interaction, texto: str):
    embed = await jobsearchfunc(interaction, texto)
    await interaction.response.send_message(embed=embed)

# COMANDO FORMULA 1
@bot.tree.command(name="formula1", description="Trae las posiciones de la F1")

# Esto es para elegir la opcion de resultado (temporada o ultima carrera)
@app_commands.describe(opcion="Elegir resultados")
@app_commands.choices(opcion=[
    app_commands.Choice(name="temporada", value="temporada"),
    app_commands.Choice(name="carrera", value="carrera")
])
async def formula1(interaction: discord.Interaction, opcion: app_commands.Choice[str]):
    await interaction.response.defer()
    response = await f1func(interaction, opcion.value)

    if response:
        # Parte el mensaje en caso de que supere los 2000 caracteres
        if len(response) > 2000:
            partes = [response[i:i+1990] for i in range(0, len(response), 1990)]
            for parte in partes:
                await interaction.followup.send(parte, ephemeral=True)
        else:
            await interaction.followup.send(response, ephemeral=True)
    else:
        await interaction.followup.send("Hubo un error o el mensaje estaba vacío.", ephemeral=True)

# COMANDO JOB POST (NATIVO DISCORD)
@bot.tree.command(name="jobpost", description="Postear un job (solo rol recruiter)")
async def jobpost(interaction: discord.Interaction):

    # Chequeamos Rol Recruiter para ejecucion del comando
    recruiter_role = discord.utils.get(interaction.guild.roles, name="Recruiter")
    if recruiter_role not in interaction.user.roles:
        await interaction.response.send_message("No tienes permisos para ejecutar este comando. Solo Recruiters pueden buscar posiciones.", ephemeral=True)
        return
    else:
        await interaction.response.send_modal(JobPostModal())


# COMANDO BULK JOB POST (VIA EXCEL FILE)
@bot.tree.command(name="bulkjobpost", description="Posteo de jobs en bulk (root only)")
async def command_bulkjobpost(interaction: discord.Interaction):

     # Solo Root puede ejecutar este comando
    root_role = discord.utils.get(interaction.guild.roles, name="root")
    if root_role not in interaction.user.roles:
        await interaction.response.send_message("No tienes permisos para ejecutar este comando.", ephemeral=True)
        return
    else:
        await bulkjobpost(interaction)

# COMANDO GOOGLE FORM JOB POST (VIA SPREADSHEET DE GOOGLE FORM)
@bot.tree.command(name="gformjobpost", description="Posteo de jobs via Google Form (root only)")
async def check_and_post_jobs(interaction: discord.Interaction):

    # Solo Root puede ejecutar este comando
    root_role = discord.utils.get(interaction.guild.roles, name="root")
    if root_role not in interaction.user.roles:
        await interaction.response.send_message("No tienes permisos para ejecutar este comando.", ephemeral=True)
        return

    await interaction.response.send_message("Discord Jobs (Gform) - 🔍 Buscando nuevos job requests...", ephemeral=True)
    
    # Chequea nuevos jobs en la sheet de respuestas de Google Form
    new_jobs = await checkforjobs()
    
    if not new_jobs:
        await interaction.followup.send("Discord Jobs (Gform) - ℹ️ No encontre ningun job nuevo", ephemeral=True)
        return
    
    # Postea los jobs nuevos en Discord
    jobs_posted = 0
    for job_data in new_jobs:
        try:
            await gformjobpost(bot, job_data)
            jobs_posted += 1
        except Exception as e:
            print(f"Discord Jobs (Gform) - ❌ Error posteando job: {e}")
    
    await interaction.followup.send(f"Discord Jobs (Gform) - ✅ Publique {jobs_posted} jobs!", ephemeral=True)

# COMANDO JOB POST PARA BORRAR OLD POSTS
# Este comando se ejecuta para eliminar job posts con mas de 30 dias de antiguedad

@bot.tree.command(name="jobpost_deleteold", description="Elimina job posts expirados (root only)")
async def jobpost_purga(interaction: discord.Interaction):

    # Solo Root puede ejecutar este comando
    root_role = discord.utils.get(interaction.guild.roles, name="root")
    if root_role not in interaction.user.roles:
        await interaction.response.send_message("No tienes permisos para ejecutar este comando.", ephemeral=True)
        return
    
    # Traemos el canal del tipo foro
    JobsChannel = int(os.getenv('JobsChannel'))
    forum_channel = bot.get_channel(JobsChannel)
    await interaction.response.defer(ephemeral=True)

    # Operacion de fecha (cuando se ejecuta el comando a mano)
    fechahoy = datetime.now(timezone.utc)
    fechaexpire = fechahoy - timedelta(days=30)
    jobsborrados = []

    # Traemos todos los threads (incluso los archivados automaticamente)
    active_threads = list(forum_channel.threads)
    archived_threads = [thread async for thread in forum_channel.archived_threads()]
    all_threads = active_threads + archived_threads

    # Buscamos los threads y los borramos
    for thread in all_threads:
        created_at = thread.created_at

        if created_at < fechaexpire:
            try:
                if not thread.archived:
                    await thread.edit(archived=True)

                await thread.delete()
                jobsborrados.append(thread)

            except Exception as e:
                print(f"Discord Jobs - ❌ Error borrando job expirado {thread.name}: {e}")

    # Mensaje de confirmacion
    print(fechahoy)
    print(f"Se ha ejecutado el comando /jobpost_deletold. Elimine {len(jobsborrados)} jobs")
    await interaction.followup.send(f"✅ Elimine {len(jobsborrados)} jobs mas antiguos que 30 dias.", ephemeral=True)


if __name__ == '__main__':
    main()

#########################################################################################
##################################### END OF CODE #######################################

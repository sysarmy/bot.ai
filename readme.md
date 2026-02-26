
BOFH - Discord community bot for Sysarmy

Version 1.6 - Feb 2026

by @Qwuor01 and @aragunde

License GPL v2 - Ver LICENSE en repositorio

---
**SUMMARY**

Este es un bot que desarrollamos para el uso diario del servidor de Discord de Sysarmy. Tiene incluidos comandos varios que venimos usando hace bastante tiempo, como tambien otros nuevos comandos de lifestyle (?).

  

Si tenes sugerencias para nuevos comandos, o mejorar los existentes, sentite libre de abrir un issue en el repo de ideas de Sysarmy: [Disneyland](https://github.com/sysarmy/disneyland), o simplemente charlando en [nuestro discord](sysar.my/discord)

  
  

Este bot funciona con la libreria de [discord.py](https://discordpy.readthedocs.io/en/stable/index.html). Usamos respuestas e interacciones en embed (si se ejecuta via slash commands) o con ctx (si se ejecuta via texto con el prefijo !). No usamos cogs porque es un quilombo. Algunos comandos funcionan de forma mas completa y linda via slash commands, pero tambien de forma mas simple via comandos con prefijo ! por la gente que se suma via IRC / slack / telegram porque reject modernity embrace tradition.

  
  

Ademas usamos SQLite para guardar todos los usuarios del server y manejar puntajes de karma, quotes, etc (lo hicimos asi porque sino no escala). Este bot esta pensado para un server con miles y miles de usuarios, por lo que se vuelve menester manejar la data de una forma mas estable y segura.

---
**DEPENDENCIAS Y LIBRERIAS**

Check requirements.txt

`pip install -r requirements.txt`

---
**FUNCIONAMIENTO DE COMANDOS**

Todos los comandos funcionan tanto como Discord slash commands como con el prefijo !: esto quiere decir que cualquier comando nuevo que se agregue en main va a ser sincronizado y cargado en la lista de slash commands disponibles al iniciar el bot. Pero si tambien se tiene que ejecutar con prefijo, se tiene que crear aparte (dentro de src/ctxcommands). Esto lo hacmos asi para simplificar la vida con el distinto manejo de variables entre "ctx" e "interaction" en Discord.py.

Algunos comandos como los de Clima, Fulbo, Cripto, etc. usan calls de APIs gratuitas por una cuestion de presupuesto. Por ese motivo limitamos las API calls por una cuestion higienica. Esto se puede modificar y va a depender de la API que se use en cada caso.

El comando help detalla instrucciones de uso para cada uno.

Comandos incluidos:

 - De feriados    --> !feriadomx !feriadoar !feriadouy !feriadocl !feriadoes
 - Lifestyle      --> !underground !subte !clima !fulbo !flip !shrug !f1
 - Economia       --> !caucho !cripto !dolar !euro !pesos
 - Karma          --> !rank !karma !kgiven !kgivers
 - Quote          --> !q !qsearch !qadd
 - Comunidad      --> !birras !nerdearla !help
 - Jobs           --> !jobs /jobsearch
---
**SISTEMA DE KARMA**


El sistema de Karma esta concebido para que los usuarios puedan recibir karma++ o karma--, y de esa manera tomarle el pulso (?) a la comunidad. Tambien para hacer un reconocimiento a los miembros del server, cuando un usuario da karma++, se le adjudica +1 de 'karmagiven'.

Como funciona? Facil:

Se puede dar karma al autor de un mensaje reaccionando con un emoji especifico en Discord:

 - Karma++ lo da el emoji ***:karmaup:***
 - Karma-- lo da el emoji ***:karmadown:***
 - Si la reaccion se quita, el karma es quitado o devuelto segun corresponda
 - Tambien se puede dar karma via texto a una palabra o usuario con ++ o --. Por ejemplo: fedora++ o usuario--


***!rank*** se utiliza ver el ranking de usuarios o palabras con mas Karma

***!kgivers*** se utiliza para ver el ranking de usuarios que mas dieron Karma

***!karma*** se utilizar para ver el karma de un usuario o palabra en particular

***!kgiven*** se utilizar para ver el karmagiven de un usuario en particular

---
**SISTEMA DE QUOTES**


El sistema de quotes funciona de una forma similar al de Karma. Se quotea un mensaje simplemente reaccionando con el emoji de discord *:quote:* y dicho mensaje se guarda en la base.

 - Si la reaccion se quita, el quote se remueve de la base de datos.
 - Un mensaje solo puede ser quoteado una vez. Si un usuario vuelve a reaccionar con :quote: a un mensaje, el quote es negado.
 - Mensajes tambien pueden ser quoteados via texto usando el comando !qadd y siguiendo un formato especifico ungido por el oraculo legendario de Sysarmy.

***!q*** se utiliza para traer un quote aleatorio del historial
***!qsearch*** se utiliza para traer un quote en base a un keyword (incluyendo usuario)
***!qsearch*** se utiliza para quotear via texto y siguiendo un formato especifico ungido por el oraculo legendario de Sysarmy.


---
**SISTEMA DE JOBS**


Desde la version 1.5 implementamos un sistema de posteo de posiciones laborales en Discord. Aquellos usuarios promovidos al rol "Recruiter" pueden postear jobs en un Forum channel mediante tres formas:

 1) Usando el comando /jobpost que dispara un form Modal (individuales)
 2) Mediante un Google Form - conexion externa via Google Sheet API (individuales)
 3) En bulk mediante un archivo xlsx
 4) Comando /jobpost_deletold elimina todos los jobs mas antiguos a 30 dias
 
 - Si bien los metodos (2) y (3) se corren automaticamente con tasks, tambien esta la posibilidad de que Discord admins ejecuten el posteo mediante los comandos /gformjobpost y /bulkjobpost

 Todo el sistema de posteo de jobs esta en .src/discordjobs/
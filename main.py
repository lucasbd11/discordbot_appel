import discord
from discord.ext import commands
import copy
import datetime
import time
import asyncio

client = commands.Bot(command_prefix = "!")

AUTHORIZED_ROLE = ["professeur"] #liste des rôles autorisés à utiliser la commande !appel
BYPASSED_ROLE = ["professeur"] #liste des rôles qui ne seront jamais comptés comme absents
saved_data = []
time_auto_refresh = 60
REMOVE_MSG_AFTER_CMD = True #condition si le bot supprime le message de avec la commande après celle ci
#TOKEN = "NjkwNTY0NzU4MDMzNzkzMDU0.XnkGEQ.H1ax_AZLvvOOad7S6wYjAQeFRGk" #PROD TOKEN
TOKEN = "Njk1MzUyMDI1MjAyMDMyNzcy.XoY7Fg.WdlEWSXqbZWJzNtf7HBmmVpHPaI" #DEV TOKEN







print("Connexion...")
@client.event
async def on_ready():
    print("Bot connecté ! ",datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")," UTC")

async def auto_refresh():
    await client.wait_until_ready()
    
    global saved_data
    while not(client.is_closed()):
        
        to_remove = []
        for data in saved_data:
            

            try:
                message = data["command_msg"]
                channel_user = data["voice_channel"]
                
                
                
                TARGETED_ROLE = ["@everyone"]
        
                if len(message.content)>6:
                    TARGETED_ROLE = message.content[7:].split(",")
                
                list_user_server = message.author.guild.members 
                
                list_user_online = [i for i in channel_user.members] 
                
                for i in list_user_online: 
                    list_user_server.pop(list_user_server.index(i))
                
                list_user_not_online = copy.copy(list_user_server) 
                
                mess = ""
                offline_count = 0
                
                for x in range(len(list_user_not_online)):
                    
                    temp_user_roles = [i.name for i in list_user_not_online[x].roles] 
    
                    if len(TARGETED_ROLE) > 1:
                        is_targeted_role = not(any(i in BYPASSED_ROLE for i in temp_user_roles)) and (min([i in temp_user_roles[1:] for i in TARGETED_ROLE]))
                    else:
                        is_targeted_role = not(any(i in BYPASSED_ROLE for i in temp_user_roles)) and (any((i in TARGETED_ROLE for i in temp_user_roles)))
    
    
                    
                    if not(list_user_not_online[x].bot) and is_targeted_role:
                    
                        if list_user_not_online[x].nick == None:
                            name = str(list_user_not_online[x])[:str(list_user_not_online[x]).find("#")]
                        else:
                            name = list_user_not_online[x].nick 
                        offline_count += 1 
                        mess += "-" + name + " ("+ list_user_not_online[x].mention +")" + "\n" 
                
                if mess != "":
    
                    if len(TARGETED_ROLE) == 1 and TARGETED_ROLE[0] != "@everyone":
                        if offline_count == 1:
                            mess = f"Il y a {offline_count} personne du groupe {TARGETED_ROLE[0]} absente dans le salon {channel_user.name}:\n\n" + mess
                        else:
                            mess = f"Il y a {offline_count} personne(s) du groupe {TARGETED_ROLE[0]} absente(s) dans le salon {channel_user.name}:\n\n" + mess 
                    else:
                        if offline_count == 1:
                            mess = f"Il y a {offline_count} personne absente dans le salon {channel_user.name}:\n\n" + mess
                        else:
                            mess = f"Il y a {offline_count} personne(s) absente(s) dans le salon {channel_user.name}:\n\n" + mess
                    
                    
                
                else:
                    mess = "Tout le monde est présent."
                
                if data["cycle"] < time_auto_refresh-1:
                    cycle_temp = data["cycle"]%2
                    if cycle_temp == 0:
                        mess += "\n\n*Actualisation automatique*   ⏳"
                    elif cycle_temp == 1:
                        mess += "\n\n*Actualisation automatique*   ⌛"
                
                
                await data["bot_message"].edit(content=mess)
            except:
                print("Erreur:\nDate:",str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " UTC","\nMessage:",message,"\nChannel:",channel_user)
            
            data["cycle"] += 1
            if data["cycle"] >= time_auto_refresh:
                date_now = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " UTC"
                print(f'Data removed:\nDate: {date_now}\nGuilde: {data["command_msg"].guild.name}\nProf: {data["command_msg"].author.name}\n------')
                to_remove += [data]
            
        for i in to_remove:
            saved_data.pop(saved_data.index(i))
        await asyncio.sleep(1)
        
        
        

@client.command(aliases = ["ap"])
async def appel(ctx,*param):
    message = ctx.message
    if not(message.author.bot): #vérification que c'est la commande et que la personne n'est pas un bot (sécurité)

        TARGETED_ROLE = ["@everyone"] #rôles dont le bot doit verifier la présence des personnes possédant (un des rôles) dans le salon

        if len(message.content)>6:
            TARGETED_ROLE = message.content[7:].split(",") #on met un seul rôle ciblé si il est passé en paramètre


        if any(n in AUTHORIZED_ROLE for n in [i.name for i in message.author.roles]): #vérification que l'auteur du message possède le rôle autorisé
        
            global saved_data
            
            if message.author.voice != None: #vérification que l'auteur du message est dans un salon vocal
                list_user_server = message.author.guild.members #création de la liste des membres du serveur
                
                list_user_online = [i for i in message.author.voice.channel.members] #création de la liste des personnes étant en dans le salon vocal
                
                for i in list_user_online: #les personnes étant dans le salon vocal sont retirées de la liste contenant toutes les personnes du serveur
                    list_user_server.pop(list_user_server.index(i))
                
                list_user_not_online = copy.copy(list_user_server) 
                
                mess = ""
                offline_count = 0
                
                for x in range(len(list_user_not_online)): #cette boucle parcour la totalité des personnes qui sont sur le serveur mais pas dans le salon vocal
                    
                    temp_user_roles = [i.name for i in list_user_not_online[x].roles] #on récupère la liste des rôles pour chaque membre qui n'est pas dans le salon vocal
                    
                    #on définit si la personne est ciblée par la commande ou pas (bon rôle)

                    if len(TARGETED_ROLE) > 1:
                        is_targeted_role = not(any(i in BYPASSED_ROLE for i in temp_user_roles)) and (min([i in temp_user_roles[1:] for i in TARGETED_ROLE]))
                    else:
                        is_targeted_role = not(any(i in BYPASSED_ROLE for i in temp_user_roles)) and (any((i in TARGETED_ROLE for i in temp_user_roles)))


                    
                    if not(list_user_not_online[x].bot) and is_targeted_role: #condition pour voir si la personne est ciblée et si elle n'est pas un bot
                    #if is_targeted_role:
                    
                        if list_user_not_online[x].nick == None: #condition pour voir si l'utilisateur s'est renommé sur le serveur ou pas (True = pas renommé, False = renommé)
                            name = str(list_user_not_online[x])[:str(list_user_not_online[x]).find("#")] #si l'utilisateur n'est pas renommé on récupère son pseudo et on retire la partie après le #
                        else:
                            name = list_user_not_online[x].nick #si l'utilisateur est renommé on récupère juste son surnom
                        offline_count += 1 #on augmente le nombre d'utilisateur qui aurait dû être présent
                        
                        mess += "-" + name + " ("+ list_user_not_online[x].mention +")" + "\n" #on génère la chaîne de caractère du message possédant les personnes non présentes
                
                
                if mess != "": #vérification qu'il y a bien des personnes absentes (sinon la chaîne de caractère n'est pas modifiée)
                    
                    
                    #ajout de l'entête du message
                    if len(TARGETED_ROLE) == 1 and TARGETED_ROLE[0] != "@everyone":
                        if offline_count == 1:
                            mess = f"Il y a {offline_count} personne du groupe {TARGETED_ROLE[0]} absente dans le salon {message.author.voice.channel.name}:\n\n" + mess
                        else:
                            mess = f"Il y a {offline_count} personne(s) du groupe {TARGETED_ROLE[0]} absente(s) dans le salon {message.author.voice.channel.name}:\n\n" + mess 
                    else:
                        if offline_count == 1:
                            mess = f"Il y a {offline_count} personne absente dans le salon {message.author.voice.channel.name}:\n\n" + mess
                        else:
                            mess = f"Il y a {offline_count} personne(s) absente(s) dans le salon {message.author.voice.channel.name}:\n\n" + mess
                    mess += "\n\n*Actualisation automatique*   ⌛"
                    
                    
                    
                    bot_message = await message.channel.send(mess) #coroutine pour envoyer le message

                    data_dict = {"bot_message":bot_message,"cycle":0,"time":time.time(),"command_msg":message,"voice_channel":message.author.voice.channel}
                    saved_data += [data_dict]
                
                else:
                    await message.channel.send("Tout le monde est présent.") #un message est envoyé si tout le monde est présent
            
            else:
                await message.channel.send("Vous devez rentrer dans un salon vocal avant d'executer cette commande.")#un  message est envoyé si la personne n'est pas dans un salon vocal
            
        else:
            await message.channel.send("Désolé "+ message.author.mention +",vous n'avez pas la premission d'utiliser cette commande.") #un message est envoyé si la personne n'a pas la permission d'utiliser la commande
        
        if REMOVE_MSG_AFTER_CMD:
            await message.delete() #on supprime le message envoyé par la personne
        


client.loop.create_task(auto_refresh())
client.run(TOKEN)


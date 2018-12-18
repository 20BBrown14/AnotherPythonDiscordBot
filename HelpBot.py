#import discord #You'll need to install this
from discord import Client
import discord
import random
import time
import subprocess #You'll need to install this and also download espeak and put in the same directory as this source code.
import threading
import os
import urllib.request
import json
from pathlib import Path
from datetime import datetime
from datetime import datetime,timedelta
import datetime
import csv
from collections import OrderedDict
from discord.utils import get
from dateutil.relativedelta import relativedelta

client = Client()

async def giphy_command(message):
  forbidden_gifs = ['/gamerescape', '/xivdb', '/giphy', '/tts', '/tenor', '/me', '/tableflip', '/unflip', '/shrug', '/nick']
  spaceIndex = message.content.find(' ')
  if spaceIndex != -1 and message.content[:spaceIndex] in forbidden_gifs:
    return
  elif spaceIndex == -1 and message.content in forbidden_gifs:
    print("Returning due to forbidden gif search")
    return
  search_params = message.content[1:]
  search_params_sb = ""
  first = True
  for i in range(0,len(search_params)):
    if search_params[i] == ' ':
      search_params_sb = search_params_sb + search_params[len(search_params_sb):i] + '+'
  search_params_sb = search_params_sb + search_params[len(search_params_sb):]
  data = json.loads(urllib.request.urlopen('http://api.giphy.com/v1/gifs/search?q='+search_params_sb+'&api_key=&limit=100').read()) #Add your own giphy API here key
  if(len(data["data"]) <=0 ):
    await client.send_message(message.author, "Sorry, but '"+message.content[1:] + "' returned no results from Giphy.")
  else:
    url = json.dumps(data["data"][random.randint(0,len(data["data"]))]["url"], sort_keys = True, indent = 4)
    await client.send_message(message.channel, url[1:len(url)-1] + ' \'' + message.content[1:] + '\' by ' + message.author.nick + ' with ' + str(len(data["data"])) + ' results')
  await client.delete_message(message)

async def ping_command(message):
  d = datetime.datetime.utcnow() - message.timestamp
  s = d.seconds*1000 + d.microseconds//1000
  await client.send_message(message.channel, "Ping: {}ms".format(s))

async def help_command(message):
  channel = message.channel
  help_message = """Here are list of available commands:
  < !help >: *Displays a list of available commands*
  < !status >: *Replys indicating I am online*
  < !ping >: *Responds with your ping*
  < !clean [amount] >: *Removes all messages from the channel this command was invoked in that were sent by me or that were commands for the me*
  < !pizza >: *Just do it*
  < !addRole [role list]>: Use this command to add yourself to a list of roles delimitted by commas
  < /[emote] >: Invoking a slash command will make me search for a relevant gif and then post it
  My main purpose to help users organize themselves with roles within the server
  <@!159785058381725696> is the creator of me, contact him if you have any questions.
  Last updated 12/7/2018""" #Change the text here to customize your help message.
  await client.send_message(channel, help_message)
  await client.delete_message(message)

async def reddit_link(message):
  await client.send_message(message.channel, "http://www.reddit.com"+message.content)
  await client.delete_message(message)

async def clean_command(message):
  channel = message.channel
  options = [channel, 50000, delete_message, message, None, None]
  await client.purge_from(channel, limit = 50000, check=lambda m: m.author.id == '335445369930514433' or m.content.startswith('!'))

async def add_role_command(message):
  rolesRaw = message.content[9:]
  rolesList = []
  dneRoles = []
  spaceIndex = 0
  while(spaceIndex != -1):
    spaceIndex = rolesRaw.find(',')
    if(spaceIndex == -1):
      rolesList.append(rolesRaw)
    else:
      rolesList.append(rolesRaw[:spaceIndex])
      rolesRaw = rolesRaw[spaceIndex+2:]

  for role in rolesList:
    role_to_add = role
    if(role_to_add.lower() == 'Admin'.lower() or role_to_add.lower() == 'Moderator'.lower()):
      await client.send_message(message.author, "You cannot add yourself to role \'" + role_to_add + "\'")
      continue
    print(role_to_add)
    roles = list(client.servers)[0].roles
    roleObject = ''
    for i in range(0, len(roles)):
      if(roles[i].name.lower() == role_to_add.lower()):
        roleObject = roles[i]
    if(roleObject == ''):
      dneRoles.append(role_to_add)
      rolesList.remove(role_to_add)
    else:
      await client.add_roles(message.author, roleObject)
  if(message.channel.name):
    await client.delete_message(message)
  if(len(rolesList) != 0):
    roleMessage = "You have been successfully added to, or already a part of, the following roles:\n"
    for role in rolesList:
      roleMessage = roleMessage + role + "\n"
    if(len(dneRoles) > 0):
      roleMessage = roleMessage + "The following roles do not exist\n"
      for role in dneRoles:
        roleMessage = roleMessage + role + "\n"
    await client.send_message(message.author, roleMessage)
  return False

@client.event
async def on_ready():
    #info
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
  if(message.author != client.user and message.content and message.channel.name):
    print(message.author.name + " said: \"" + message.content + "\" in #" + message.channel.name + " @ " + time.ctime())
  elif(message.author != client.user):
    print(message.author.name + " said: \"" + message.content + "\" privately")
  if(message.content.startswith('!status')):
    await client.send_message(message.channel, 'I am here')
  elif(message.content.startswith('!help')):
    await help_command(message)
  elif(message.content.startswith('!ping')):
    await ping_command(message)
  elif(message.content.startswith('/r/')):
    await reddit_link(message)
  elif(message.content.startswith('!clean')):
    await clean_command(message)
  elif(message.content.startswith('!pizza')):
    await client.send_message(message.channel, 'Pizza? Who\'s paying for this? Not me.')
  elif(message.content.lower().startswith('!addrole')):
    await add_role_command(message)
  elif(message.content.startswith('/')):
    await giphy_command(message)

client.run("") #Add your own bot's token here

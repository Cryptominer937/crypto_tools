#!/usr/bin/env python3
# Copyright (c) 2018 Lyndros
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
import discord
import requests
import coinmarketcap
import json
import yaml
import argparse

from urllib.request         import urlopen
from discord.ext.commands   import Bot
from discord.ext            import commands
from datetime               import datetime
from prettytable            import PrettyTable

#Add the configuration file to our python program
parser = argparse.ArgumentParser()
parser.add_argument("config_file", help="The configuration file to be loaded.")
args = parser.parse_args()

#Parse the configuration file
with open(args.config_file, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

Client = discord.Client()
client = commands.Bot(command_prefix = "!")

lista_comandos = {
  "AYUDA":        "Muestra esta ayuda.",
  "PRECIO":       "Muestra el precio actual de la moneda.",
  "BALANCE":      "Muestra el balance actual de todas las cuentas.",
  "RENDIMIENTO":  "Muestra el rendimiendo actual de los MNs"
}

def get_running_days(date_epoch):
    #Starting date
    d0 = datetime.strptime(date_epoch, '%d/%m/%Y')
    #Current date
    d1 = datetime.strptime(datetime.now().strftime('%d/%m/%Y'),'%d/%m/%Y')
    delta = d1 - d0

    return delta.days

def get_balance(address):
    url = cfg['COIN']['explorer_url'] + address
    req = requests.get(url)
    status_code = req.status_code
    if status_code == 200:
        #Limit to 6 decimals
        return round(float(json.loads(req.text)['balance']),cfg['COIN']['decimals'])
    else:
        return None

def mostrar_ayuda():
    message="\n+Lista de comandos:\n"
    for comando in sorted(dict.keys(lista_comandos)):
        message+='*{0:14}'.format(comando)+lista_comandos[comando]+'\n'

    return message

def mostrar_precio():
    Now = datetime.now()
    market = coinmarketcap.Market()
    coin = market.ticker(cfg['COIN']['name'], convert="EUR")
    message = "\n+Marketcap " + cfg['COIN']['acronym'] + "(" + str('{:%d/%m/%Y - %H:%M:%S}'.format(datetime(Now.year, Now.month, Now.day, Now.hour, Now.minute, Now.second))) + ")" + \
    "\nRanking       = " + coin[0]['rank'] + \
    "\nPrecio EUR    = " + coin[0]['price_eur'] + " €" + \
    "\nPrecio BTC    = " + coin[0]['price_btc'] + \
    "\nMarketCap EUR = " + str('{:,.2f}'.format(float(coin[0]['market_cap_eur']))) + " €" + \
    "\n% cambio 1h   = " + coin[0]['percent_change_1h'] + " %" + \
    "\n% cambio 24h  = " + coin[0]['percent_change_24h'] + " %" + \
    "\n% cambio 7d   = " + coin[0]['percent_change_7d'] + " %"

    return message

def mostrar_balance():
    #Variable para calcular el balance total
    Total_Balance = 0.0

    #Construimos la dichosa tablita
    Tabla = PrettyTable()
    Tabla.field_names = ["MN", "Balance"]

    #Get balance for all nodes
    for mn in cfg['MASTERNODES']:
        MN_Current_Coins = get_balance(mn['address'])
        Total_Balance += MN_Current_Coins
        Tabla.add_row([mn['name'], "{0:.{1}f}".format(MN_Current_Coins, cfg['COIN']['decimals'])])

    #Get balance for other addresses
    for oaddr in cfg['OTHER_ADDRESSES']:
        OADDR_Current_Coins = get_balance(oaddr['address'])
        Total_Balance += OADDR_Current_Coins
        Tabla.add_row([oaddr['name'], "{0:.{1}f}".format(OADDR_Current_Coins, cfg['COIN']['decimals'])])

    #Ponemos todo en el mensajito de vuelta
    message = '\n' + \
    '+Balance ' + cfg['COIN']['acronym'] +'\n' + \
    Tabla.get_string() + '\n'  \
    '-Total:  '+"{0:.{1}f}".format(Total_Balance, cfg['COIN']['decimals'])

    return message

def mostrar_rendimiento():
    #Coge el valor actual de la moneda
    market = coinmarketcap.Market()
    coin = market.ticker(cfg['COIN']['name'], convert="EUR")

    #Para calcular el total
    Total_EUR_Day   = 0.0
    Total_Coins_Day = 0.0

    #Construimos la dichosa tablita
    Tabla = PrettyTable()
    Tabla.field_names = ["MN", cfg['COIN']['acronym']+"/Dia", "EUR/Dia"]

    #Get balance for all nodes
    for mn in cfg['MASTERNODES']:
        MN_Init_Date     = mn['setup_date']
        MN_Initial_Coins = mn['setup_balance']
        MN_Current_Coins = get_balance(mn['address'])
        MN_Running_Days  = get_running_days(MN_Init_Date)+1
        MN_Coins_Day     = round((MN_Current_Coins-MN_Initial_Coins)/MN_Running_Days, cfg['COIN']['decimals'])
        MN_EUR_Day       = round(MN_Coins_Day*float(coin[0]['price_eur']), cfg['COIN']['decimals'])
        Tabla.add_row([mn['name'], "{0:.{1}f}".format(MN_Coins_Day, cfg['COIN']['decimals']), "{0:.{1}f}".format(MN_EUR_Day, 2)])
        #Total Computation
        Total_EUR_Day    += MN_EUR_Day
        Total_Coins_Day  += MN_Coins_Day

    #Ponemos todo en el mensajito de vuelta
    message = "\n" + \
    "+Rendimiento MNs\n" + \
    Tabla.get_string()+ '\n'  \
    '-Total:  '+"{0:.{1}f}".format(Total_Coins_Day, cfg['COIN']['decimals'])+"     "+"{0:.{1}f}".format(Total_EUR_Day, 2)

    return message

def comando_bot(cmd):
    if   (cmd == "AYUDA"):
        message = mostrar_ayuda()
    elif (cmd == "PRECIO"):
        message = mostrar_precio()
    elif (cmd == "BALANCE"):
        message = mostrar_balance()
    elif (cmd == "RENDIMIENTO"):
        message =  mostrar_rendimiento()
    else:
        message = "\n-Error! Comando desconocido.\nTeclee '/bot ayuda' para mostrar una lista de los comandos disponibles."

    return message

@client.event
async def on_ready():
    print(cfg['COIN']['name'] + " BOT funcionando")

@client.event
async def on_message(message):
    if (message.content.upper()[0:5]=="/BOT "):
        return_message = comando_bot(message.content.upper()[5:])
        await client.send_message(message.channel, "```diff" + return_message + "\n```")

client.run(cfg['DISCORD']['api_key'])
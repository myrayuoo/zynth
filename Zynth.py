import os
import sys
import json
import time
#import cursor
import requests
import threading
import discord_webhook
from colorama import Fore as c
from discord import Webhook, RequestsWebhookAdapter

#ZYNTH---------------

pr = "\033[38;5;49m" #primary
sc = "\033[38;5;41m" #secondary
inp = "\033[38;5;35m" #input colour

p = f"    {pr}[Z] {sc}" #prefix
pi = f"    {pr}[Z] {inp}" #input prefix
su = f"    {pr}[+]{sc} " #success
er = f"    {pr}[!]{sc} " #error

debug_mode = True

#FUNCTIONS---------

def launch():
    #cursor.cursor.hide()
    os.system('mode con: cols=50 lines=19')
    os.system("title "+gettitle("Zynth"))
    try:
        open("config.json")
    except FileNotFoundError:
        open("config.json", "w").write(json.dumps({
            "name": "Zynth",
            "url": "https://raw.githubusercontent.com/xellu/zynth/main/zynth.png",
            "icon": "",
            "hider": 0,
            "use_default": 0
        }))
    selector()

def cls():
    os.system("cls")

def gettitle(name):
    return "⠀"*int(int(os.get_terminal_size().columns/2)-len(name)*2)+name

def config_edit(cfg_name=None, cfg_url=None, cfg_icon=None, cfg_hider=None, cfg_use_default=None):
    config_new = json.loads(open("config.json", "r", encoding="utf-8").read())
    if cfg_name == None:
        cfg_name = config_new["name"]
    if cfg_url == None:
        cfg_url = config_new["url"]
    if cfg_icon == None:
        cfg_icon = config_new["icon"]
    if cfg_hider == None:
        cfg_hider = config_new["hider"]
    if cfg_use_default == None:
        cfg_use_default = config_new["use_default"]
    cfg = {
    "name": cfg_name,
    "url": cfg_url,
    "icon": cfg_icon,
    "hider": cfg_hider,
    "use_default": cfg_use_default
    }
    open("config.json", "w", encoding="utf-8").write(json.dumps(cfg, indent=5))


#GUIS N STUFF--------------

def title():
    print(pr)
    width = os.get_terminal_size().columns
    text = """███████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗
╚══███╔╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝██║  ██║
  ███╔╝  ╚████╔╝ ██╔██╗ ██║   ██║   ███████║
 ███╔╝    ╚██╔╝  ██║╚██╗██║   ██║   ██╔══██║
███████╗   ██║   ██║ ╚████║   ██║   ██║  ██║
╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝"""
    for x in text.splitlines():
        print(x.center(width))
    print(sc)
    print(" "+"─"*int(width-2))

def settings():
    while True:
        cls()
        title()
        print(f"""
    {pr}[1] {sc}Webhook Name {pr}[5] {sc}Use default URL
    {pr}[2] {sc}Webhook Icon {pr}[6] {sc}Restart
    {pr}[3] {sc}Default URL  {pr}[7] {sc}Exit
    {pr}[4] {sc}URL Hider    {pr}[8] {sc}Main Menu
    """)
        s = input(pi).lower()
        if s == "1":
            config_edit(cfg_name=str(input(f"{p}New name: ")))
            print(f"{p}Webhook name was changed!")
        elif s == "2":
            config_edit(cfg_icon=str(input(f"{p}Icon URL: "+inp)))
            print(f"{p}Webhook Icon was changed!")
        elif s == "3":
            config_edit(cfg_url=str(input(f"{p}Webhook URL: "+inp)))
            print(f"{p}Default URL was changed!")
        elif s == "4":
            if json.loads(open("config.json", "r", encoding="utf-8").read())["hider"] == 1:
                config_edit(cfg_hider=0)
                print(f"{p}Toggled off URL Hider!")
            else:
                config_edit(cfg_hider=1)
                print(f"{p}Toggled off URL Hider!")
        elif s == "5":
            if json.loads(open("config.json", "r", encoding="utf-8").read())["use_default"] == 1:
                config_edit(cfg_use_default=0)
                print(f"{p}Disabled usage of Default URL!")
            else:
                config_edit(cfg_use_default=1)
                print(f"{p}Enabled usage of Default URL!")
        elif s == "6":
            scriptname =  os.path.basename(sys.argv[0])
            os.system(f"""""{scriptname}""""")
            os._exit(0)
        elif s == "7":
            os._exit(0)
        elif s == "8":
            break
        else:
            break
        if s != "6":
            time.sleep(1)

def geturl(ask=False):
    while True:
        h = inp
        if json.loads(open("config.json", "r", encoding="utf-8").read())["hider"] == 1:
            h = c.BLACK
        if ask == "deny":
            url = input(f"{p}Webhook URL: "+h)
            if "https://discord.com/api/webhooks/" in url:
                return url
            print(f"{p}Invalid URL format")
        else:
            if json.loads(open("config.json", "r", encoding="utf-8").read())["use_default"] == 1:
                if "https://discord.com/api/webhooks/" in json.loads(open("config.json", "r", encoding="utf-8").read())["url"]:
                    if ask:
                        if input(f"{p}Do you wish to use Default URL? (y/n): ") == "y":
                            return json.loads(open("config.json", "r", encoding="utf-8").read())["url"]
                    else:
                        print(f"{p}Prefilled webhook url")
                        return json.loads(open("config.json", "r", encoding="utf-8").read())["url"]
            url = input(f"{p}Webhook URL: "+h)
            if "https://discord.com/api/webhooks/" in url:
                return url
            print(f"{p}Invalid URL format")

def getamount(label="Amount", maximum=0):
    while True:
        amount = input(f"{p}{label}: ")
        if amount == "":
            return 0
        try:
            amount = int(amount)
            if maximum != 0:
                if amount > maximum:
                    amount=maximum
        except:
            print(f"{p}Invalid number selection")
        else:
            return amount

def gui():
    title()
    print(f"""
    {pr}[1] {sc}Options      {pr}[7] {sc}Upload File
    {pr}[2] {sc}Check        {pr}[8] {sc}Timer
    {pr}[3] {sc}Delete       {pr}[9] {sc}Counter
    {pr}[4] {sc}Spam         {pr}[10] {sc}Chat
    {pr}[5] {sc}Message      {pr}[11] {sc}Mass Spam 
    {pr}[6] {sc}Embed        {pr}[12] {sc}Mass Send
""")        

def selector():
    while True:
        try:
            cls()
            gui()
            s = input(pi).lower()
            if s == "1":
                settings()
            elif s == "2":
                checker()
            elif s == "3":
                deleter()
            elif s == "4":
                spammer()
            elif s == "5":
                sender()
            elif s == "6":
                embed_sender()
            elif s == "7":
                file_upload()
            elif s == "8":
                timer()
            elif s == "9":
                counter()
            elif s == "10":
                chat()
            elif s == "11":
                multispammer()
            elif s == "12":
                multisender()
        except Exception as error:
            print(f"{p}An error was registered")
            if debug_mode:
                print(error)
            time.sleep(1)
        
        

#WEBHOOK UTILS--------------------

def multisender():
    url_amount = getamount("Webhook Amount")
    urls = []
    for i in range(url_amount):
        urls.append(geturl(ask="deny"))
    msg = input(f"{p}Message: ")
    input(f"{p}Press enter to send"+c.BLACK)
    for url in urls:
        send(url,msg)
    print(f"{p}{len(urls)} messages were sent")
    time.sleep(1)
    
def multispammer():
    url_amount = getamount("Webhook Amount")
    urls = []
    for i in range(url_amount):
        urls.append(geturl(ask="deny"))
    amount = getamount()
    msg = input(f"{p}Message: ")
    input(f"{p}Press enter to start spamming"+c.BLACK)
    for i in range(amount):
        for url in urls:
            threading.Thread(target=send, args=(url, msg)).start()
    print(f"{p}{int(amount*len(urls))} messages were sent")
    time.sleep(1)

def chat():
    url = geturl()
    name = json.loads(open("config.json", "r", encoding="utf-8").read())["name"]
    icon = json.loads(open("config.json", "r", encoding="utf-8").read())["icon"]
    print(f"{p}Use '!help' to view all of the commands\n")
    while True:
        text = input(f"{pi}").replace("\\n", "\n").replace("\\033", "\033")
        if text == "!help":
            help_page = """Zynth Command list:
!help - this page
!name - changes the webhook name
!avatar - changes the avatar url
!exit - leaves the chat"""
            for x in help_page.splitlines():
                print(f"{p}{x}")
        elif text == "!name":
            newname = input(f"{p}New username: ")
            if newname != "" or newname != " ":
                name = newname
        elif text == "!avatar":
            icon = input(f"{p}Icon URL: ")
            print()
        elif text == "!exit":
            return
        else:
            threading.Thread(target=chatsend, args=(url,text,name,icon)).start()
            
def chatsend(url, text, name, icon):
    while True:
        r = requests.post(url, json={"content": text, "username": name, "avatar_url": icon})
        if r.status_code != 429:
            break
        else:
            if debug_mode:
                print("ratelimited")

def counter():
    url = geturl()
    amount = getamount()
    delay = getamount("Delay (ms)")
    for i in range(amount):
        send(url, str(i+1))
        time.sleep(delay/1000)
    print(f"{p}Counted to number {amount}")
    time.sleep(1)

def timer():
    url = geturl()
    amount = getamount("Time (min)")
    amount = amount*60
    send(url=url, msg=f"<t:{int(time.time()+amount)}:R>")
    print(f"{p}Timer started")
    time.sleep(1)

def file_upload():
    hook = discord_webhook.DiscordWebhook(url=geturl(), username=json.loads(open("config.json", "r", encoding="utf-8").read())["name"], icon_url=json.loads(open("config.json", "r", encoding="utf-8").read())["icon"])
    file_amount = getamount("File amount", 10)
    files = 0
    for i in range(file_amount):
        path = input(f"{p}File Path: ")
        try:
            open(path)
        except:
            print(f"{p}File not found")
        else:
            files += 1
            hook.add_file(file=open(path, "rb").read(), filename=path)
    if files > 0:
        hook.execute()
        print(f"{p}{file_amount} files were sent")
    else:
        print(f"{p}No files were provided")
    time.sleep(1)

def embed_sender():
    url = geturl()
    hook = discord_webhook.DiscordWebhook(url=url, username=json.loads(open("config.json", "r", encoding="utf-8").read())["name"], icon_url=json.loads(open("config.json", "r", encoding="utf-8").read())["icon"])
    if checker(url)==False:
        print(f"{p}Webhook doesn't work")
        time.sleep(1)
        return
    print(f"{p}Press enter to skip settings\n")
    message = input(f"{p}Message: ").replace("\\n", "\n")
    if message != "":
        hook.set_content(message)
    embed_amount = getamount("Embed amount", maximum=10)
    for i in range(embed_amount):
        if embed_amount > 1:
            print(f"\n{p}Embed {i+1}: ")
        title = input(f"{p}Title: ")
        desc = input(f"{p}Description: ").replace("\\n", "\n")
        color = input(f"{p}Hex Color: #")
    
        embed = discord_webhook.DiscordEmbed(title=title, description=desc, color=color)

        field_amount = getamount("Field amount")
        for i in range(field_amount):
            field_name = input(f"{p}Field name ({i+1}): ")
            field_value = input(f"{p}Field value ({i+1}): ").replace("\\n", "\n")
            embed.add_embed_field(name=field_name, value=field_value)

        author = input(f"{p}Author: ")
        if author != "":
            author_url = input(f"{p}Author URL: "+inp)
            author_icon = input(f"{p}Author Icon URL: "+inp)
            embed.set_author(name=author, url=author_url, icon_url=author_icon)
        
        footer_text = input(f"{p}Footer: ")
        if footer_text != "":
            embed.set_footer(text=footer_text)
        timestamps = input(f"{p}Enable timestamps? (y/n): ")
        if "y" in timestamps:
            embed.set_timestamp()
        hook.add_embed(embed)
        if embed_amount > 1:
            print(f"{p}Embed {i+1} finished")
    input(f"{p}Press enter to send"+c.BLACK)
    hook.execute()
    print(f"{p}{embed_amount} embeds were sent")
    time.sleep(1)

def sender():
    cls()
    title()
    url = geturl()
    if checker(url) == False:
        print(f"{er}Webhook doesn't work")
        time.sleep(1)
        return
    msg = input(f"{p}Message: ").replace("\\n", "\n")
    send(url, msg)
    print(f"{p}Message sent")
    time.sleep(1)

def spammer():
    cls()
    title()
    url = geturl()
    if checker(url) == False:
        print(f"{er}Webhook doesn't work")
        time.sleep(1)
        return
    amount = getamount()
    msg = input(f"{p}Message: ").replace("\\n", "\n")

    for i in range(amount):
        threading.Thread(target=send, args=(url, msg)).start()
    print(f"{p}Spamming in progress")
    time.sleep(1)

def send(url, msg):
    webhook_name = json.loads(open("config.json", "r", encoding="utf-8").read())["name"]
    avatar_url = json.loads(open("config.json", "r", encoding="utf-8").read())["icon"]
    while True:
        r = requests.post(url, json={"content": msg, "username": webhook_name, "avatar_url": avatar_url})
        if r.status_code == 429:
            time.sleep(5)
            if debug_mode:
                print("ratelimited")
        else:
            if debug_mode:
                print("message sent")
            break


def deleter():
    cls()
    title()
    url = geturl(ask=True)
    if checker(url):
        Webhook.from_url(url, adapter=RequestsWebhookAdapter()).delete()
        print(f"{su}Webhook deleted")
    else:
        print(f"{er}Webhook doesn't work")
    time.sleep(1)

def checker(url=None):
    if url == None:
        cls()
        title()
        url = geturl(ask=True)
        r = requests.post(url).status_code
        if r == 400:
            print(f"{su}Webhook is working")
        else:
            print(f"{er}Webhook doesnt work")
        time.sleep(1)
    else:
        r = requests.post(url).status_code
        if r == 400:
            return True
        else:
            return False


# Made by Xellu ♥
launch()
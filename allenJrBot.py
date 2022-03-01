import os
import discord
from discord.message import Attachment 
from dotenv import load_dotenv
from handleGuildData import DataHandle
from handleDataBase import DatabaseHandle

load_dotenv()
TOKEN =os.getenv('DISCORD_TOKEN')
GUILD_NAME=os.getenv('DISCORD_GUILD')
GUILD_ID=os.getenv('GUILD_ID')
AUTHOR_ID= int(os.getenv('AUTHOR_ID'))
COLOUM_LENGTH = 17
ITEM_PER_LINE = 4
MAX_LINE=5
database_handle = DatabaseHandle()



client = discord.Client()
data_handle = DataHandle()


def InitGuildData(guild_name):
    guild_data=dict()
    guild_data['name']=guild_name
    guild_data['prefix']='!a'
    return guild_data

def setPrefix(message):
    global data_handle
    new_prefix = message.content.split()[1]
    data_handle.setPrefix(message.guild.name,new_prefix)
    return new_prefix

def getHelpMessage():
    return f">>>\
    Allen Jr. Bot help command  \n\
    **Admin command:**          \n\
    **add** , **prefix** , **add**    \n\
    **General command:**        \n\
    **map**  "

def getRefName(name):
    tokens = ('-'.join(name.split(' ')).split('-'))
    tokens = [token[0].upper() for token in tokens]
    return ''.join(tokens)

def searchMap(message):
    map_name = message.split(' ')
    map_name = ' '.join.map_name[1:].strip()
    map_name = '-'.join(map_name.split(' '))
    ref_name = [token[0] for token in map_name.split('-')]
    ref_name=''.join(ref_name)
    ref_name.uppder()
    filter={'name':map_name}
    
def fixCaseMapName(name):
    tokens=name.split('-')
    tokens=[token[0].upper()+token[1:] for token in tokens]
    return'-'.join(tokens)

def normalizeSearchMapResponse(response):
    response_data = response
    attachment=None
    response_length = len(response_data)
    if(response_length==0):
        response=">>> Zero zone was found have the similar name"
    elif(response_length==1):
        response_data= response_data[0]
        response= f">>> The map contain these information:       \n\
            `Name           : ` {fixCaseMapName(response_data['name'])}          \n\
            `Tier           : ` {response_data['tier']}          \n\
            `Wood           : ` {response_data['wood']}          \n\
            `Ore            : ` {response_data['ore']}           \n\
            `Fiber          : ` {response_data['fiber']}         \n\
            `Hide           : ` {response_data['hide']}          \n\
            `Stone          : ` {response_data['stone']}         \n\
            `Green chest    : ` {response_data['green_chest']}   \n\
            `Blue chest     : ` {response_data['blue_chest']}    \n\
            `Gold chest     : ` {response_data['gold_chest']}    \n\
            `Green dungeon  : ` {response_data['solo_dungeon']}  \n\
            `Group dungeon  : ` {response_data['group_dungeon']} \n\
            `Avalon dungeon : ` {response_data['ava_dungeon']}   \n\
            "
        if(response_data['map_url']):
            attachment = response_data['map_url']
    else:
        response=f">>> The map you seek for isn't exist in our database\n\
        Maybe it's one of these map or concider to contact addmin to add it \n\
        "
        for map in response_data:
            response+=f"`{fixCaseMapName(map['name'])}` ,"
        response = response[:-1]
    return (response,attachment)

def getAddDataFormat():
    return ">>> \
    The `add` command format have the following data:\n\
    <prefix>add `name` , `tier(0 if unchange)` , `woods` , `fibers` , `ores` , `stones` , `hides` , \n\
    `green_chests` , `blue_chests` , `gold_chest` , `solo_dungeon` , `group_dungeon` , 'ava_dungeon'\n\
    `<image attatchment(optional)>`\
    "

def fixedWidth(string_data,fixed_length=COLOUM_LENGTH):
    return(string_data+(fixed_length-len(string_data))*' ')

def getMapStatistic(map):
    total_map = len(map)
    line_count = total_map//ITEM_PER_LINE+1
    secment_count = line_count//MAX_LINE+1
    response = []
    for i in range(secment_count):
        line='>>> '
        for j in range(i*MAX_LINE,(i+1)*MAX_LINE):
            for k in range(j*ITEM_PER_LINE,(j+1)*ITEM_PER_LINE):
                if(k<total_map):
                    line+=f"`{fixedWidth(map[k])}`\t"
                    if((k+1)%ITEM_PER_LINE==0):
                        line+='\n'
                else:
                    break
        if(len(line)>6):
            response.append(line)
    
    return response


def getDisplayMapList(response,tier=0):
    response = list(response)
    response_string = []
    tier4_map=[]
    tier5_map=[]
    tier6_map=[]
    tier7_map=[]
    tier8_map=[]
    for map in response:
        if(map['tier']==4):
            tier4_map.append(map['name'])
        if(map['tier']==5):
            tier5_map.append(map['name'])
        if(map['tier']==6):
            tier6_map.append(map['name'])
        if(map['tier']==7):
            tier7_map.append(map['name'])
        if(map['tier']==8):
            tier8_map.append(map['name'])
    response_string.append('>>> Ava map list:\n')
    tier4_report = getMapStatistic(tier4_map)
    tier5_report = getMapStatistic(tier5_map)
    tier6_report = getMapStatistic(tier6_map)
    tier7_report = getMapStatistic(tier7_map)
    tier8_report = getMapStatistic(tier8_map)
    if(tier==4 or tier==0):
        response_string.append('> **Tier 4**')
        for item in tier4_report:
            response_string.append(item)
    
    if(tier==5 or tier==0):
        response_string.append('> **Tier 5**')
        for item in tier5_report:
            response_string.append(item)
    
    
    if(tier==6 or tier==0):
        response_string.append('> **Tier 6**')
        for item in tier6_report:
            response_string.append(item)

    
    if(tier==7 or tier==0):
        response_string.append('> **Tier 7**')
        for item in tier7_report:
            response_string.append(item)
    
    
    if(tier==8 or tier==0):
        response_string.append('> **Tier 8**')
        for item in tier8_report:
            response_string.append(item)
    return response_string



@client.event
async def on_ready():
    if(not data_handle.isExist(GUILD_NAME)):
        guild_data = InitGuildData(GUILD_NAME)
        data_handle.setGuildData(GUILD_NAME , guild_data)
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    # print(GUILD_ID)
    # print(message.guild.id)
    if(message.author==client.user):
        return 
    if(message.guild.id==int(GUILD_ID)):
        guild_data = data_handle.getGuildData(GUILD_NAME)
        prefix_length = len(guild_data['prefix'])
        if(message.content[:prefix_length]==guild_data['prefix']):
            prefix =message.content[:prefix_length]
            command = message.content.split()[0][prefix_length:]
            message_content = ' '.join(message.content.split()[1:])

            if(command=='help'):
                help_message= getHelpMessage()
                await message.channel.send(help_message)
                pass
            elif(command=='prefix'):
                new_prefix=setPrefix(message)
                # await message.channel.send('`test\nthis\nis\n a test sample`')

            elif(command=='map'):
                name = message_content
                response = database_handle.getMapByName(name)
                response = list(response)
                if(len(response)==0):
                    response = database_handle.getMapByRefName(name)
                    response = list(response)
                (response,attachment) = normalizeSearchMapResponse(response)
                await message.channel.send(response)
                if(attachment is not None):
                    await message.channel.send(attachment)
            elif(command =='maplist'):
                if(len(message_content)!=0):
                    tier = int(message_content)
                else:
                    tier =0
                
                response = database_handle.getMapList()
                response = getDisplayMapList(response,tier)
                for info in response:
                    await message.channel.send(info)
            elif(command=='calldaddy' and message.author.id==AUTHOR_ID):
                await message.channel.send('Dada')
            elif(command=='add' and message.author.id==AUTHOR_ID):
                response='>>> Your text is in wrong format\nPlease use <prefix>add help to know more '
                if(message_content =='help'):
                    response = getAddDataFormat()
                else:
                    data = message_content.split(',')
                    tier = int(data[1])
                    map_data={
                        'name':data[0],
                        'ref_name':getRefName(data[0]),
                        'wood':data[2],
                        'fiber':data[3],
                        'ore':data[4],
                        'stone':data[5],
                        'hide':data[6],
                        'green_chest':data[7],
                        'blue_chest':data[8],
                        'gold_chest':data[9],
                        'solo_dungeon':data[10],
                        'group_dungeon':data[11],
                        'ava_dungeon':data[12]
                    }
                    if(tier!=0):
                        map_data['tier']=tier
                    if(message.attachments):
                        map_data['map_url']=message.attachments[0].url
                    
                    database_handle.addMapData(map_data)
                    response = '>>> Add data successfully\n'+'`'+data[0]+'` have been listed in the database'
                
                await message.channel.send(response)



            
client.run(TOKEN)
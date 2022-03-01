file_path = './avaMap.csv'
out_path = './op_av.csv'
file_stream = open(file_path,'r')
o_stream = open(out_path,'w+')
header = file_stream.readline()
for line in file_stream:
    data = line[:-1].split(',')
    data = ['0' if element=='' else element for element in data]
    data = [int(element) if len(element)==1 else element for element in data]
    data[1] = int(data[1][1:])
    # print(data)
    temp_dict = {
        'map_url':'',
        'name':data[0],
        'tier':data[1],
        'wood':data[2],
        'stone':data[3],
        'ore':data[4],
        'hide':data[5],
        'fiber':data[6],
        'green_chest':data[7],
        'blue_chest':data[8],
        'gold_chest':data[9],
        'solo_dungeon':data[10],
        'group_dungeon':data[11],
        'ava_dungeon':data[12]
    }
    new_token = []
    new_token.append(str(temp_dict['name']))
    new_token.append(str(temp_dict['tier']))
    new_token.append(str(temp_dict['wood']))
    new_token.append(str(temp_dict['fiber']))
    new_token.append(str(temp_dict['ore']))
    new_token.append(str(temp_dict['stone']))
    new_token.append(str(temp_dict['hide']))
    new_token.append(str(temp_dict['green_chest']))
    new_token.append(str(temp_dict['blue_chest']))
    new_token.append(str(temp_dict['gold_chest']))
    new_token.append(str(temp_dict['solo_dungeon']))
    new_token.append(str(temp_dict['group_dungeon']))
    new_token.append(str(temp_dict['ava_dungeon']))
    token_line=','.join(new_token)
    o_stream.write(token_line)
    o_stream.write('\n')


file_stream.close()
o_stream.close()
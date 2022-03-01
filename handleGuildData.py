import  json
import os 
class DataHandle:
    def __init__(self):
        self.data_path = './data'
        pass 
    def getGuildFilePath(self,guild_name):
        return self.data_path+'/guildData/'+guild_name+'.json'

    def getGuildData(self,guild_name):
        file_stream = open(self.getGuildFilePath(guild_name),'r')
        guild_data = json.load(file_stream)
        file_stream.close()
        return guild_data
    
    def setGuildData(self,guild_name,guild_data):
        file_stream = open(self.getGuildFilePath(guild_name),'w+')
        json.dump(guild_data,file_stream)
        file_stream.close()

    def isExist(self,guild_name):
        if(os.path.exists(self.getGuildFilePath(guild_name))):
            return True
        return False

    def setPrefix(self,guild_name,prefix):
        if(self.isExist(guild_name)):
            guild_data = self.getGuildData(guild_name)
            guild_data['prefix'] = prefix
            self.setGuildData(guild_name,guild_data)


    
import json

def dump(data:dict, filename:str, path:str='temp/'):
    f = open(path+filename+".json", "w")
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()
import json, os
fileName = "save.json"
def LoadProgress():
        if not os.path.exists(fileName):
            return {"coins":0}

        with open(fileName, "r") as file:
            try:
                data = json.load(file)
                coins = data.get("coins",0)
                return {"coins":coins}
            except json.JSONDecodeError:
                return{"coins":0}

def saveProgress(data):
    with open(fileName, "w") as file:
        json.dump(data, file)

    
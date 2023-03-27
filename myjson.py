import json;
class Json:
    def __init__(self,file):
        self.file=file;
        self.file;
    def __str__(self) -> str:
        pass;

    def guardar(self,lista,file=None):
        if file == None:
            with open(self.file, "w") as file:
                json.dump(lista,file,indent=4);
        else:
            with open(file, "w") as file:
                json.dump(lista,file,indent=4)

    def cargar(self,file=None):
        if file == None:            
            with open(self.file, "r") as file:
                p = file.read();
                if p != "":
                    return json.loads(p);
        else:            
            with open(file, "r") as file:
                p = file.read()
                if p != "":
                    return json.loads(p);


    def limpiar(self,file):
            with open(file, "w") as file:
                json.dump([],file,indent=4);
if __name__ == "__main__":
    var = Json("prueba.json");
    var.guardar();
    if var.cargar() != None:
        print(var.cargar());
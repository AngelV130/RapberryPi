from myjson import Json;
class Lista(Json):
    def __init__(self,nombre):
        self.lista = [];
        super().__init__(nombre);
    
    def __str__(self) -> str:
        return f"{self.lista}";

    def agregar(self,add):
        self.lista.append(add);

    def modificar(self,indice,add):
        if type(indice) == int:
            self.eliminar(indice);
            self.lista.insert(indice,add);
        else:
            print(indice);
            
    def eliminar(self,indice):
        if type(indice) == int:
            self.lista.pop(indice);
        else:
            print(indice);

    def get_lista(self):
        li = []
        for li in self.lista:
            li.append(li)
        return li
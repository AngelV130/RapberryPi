from datetime import datetime;
import pymongo;
class ConexionMongo:
    def __init__(self,db,collection):
        try:
            self.conexion = pymongo.MongoClient("mongodb+srv://Angel:angel123@ejemplo.l9sfrvy.mongodb.net/?retryWrites=true&w=majority",serverSelectionTimeoutMS=1000);
            self.db = self.conexion[db];
            self.collection = self.db[collection];
            self.verificacion = True;
            print("conectado exitosamente")
        except pymongo.errors.ServerSelectionTimeoutError as  errorTiempo:
            print("Tiempo Exedido ");
            self.verificacion = False;
        except pymongo.errors.OperationFailure as error: 
            print("Error de Identificacion");
            self.verificacion = False;
        except pymongo.errors.InvalidURI as error:
            print("error URL");
            self.verificacion = False;
        except pymongo.errors.ConfigurationError as error:
            print("No hay conexion");
            self.verificacion = False;
    def agregarCollection(self,datos):
        if type(datos) != list and type(datos) == dict:
            print(self.collection.insert_one(datos));
        elif type(datos) == list:
            indice = 0;
            while indice < len(datos):
                if type(datos[indice]) != dict:
                    datos.pop(indice);
                indice = indice + 1;
            print(self.collection.insert_many(datos));
        else:
            print("No se pudo insertar");

    def traerDatos(self,query=None):
        lista = [];
        for x in self.collection.find({}):
            lista.append(x);
        if len(lista) >= 1:
            return lista;
        else:
            return None;
    
    def cerrarConexion(self):
        self.conexion.close();

#fecha = datetime(day=datetime.now().day,month=datetime.now().month,year=datetime.now().year,hour=datetime.now().hour,minute=datetime.now().minute,second=datetime.now().second);
#mongo = ConexionMongo("ejemplo_proyecto","ejemplo");
#add = {"_id":130,"nombre":"nom2","fecha":fecha}
#mongo.agregarCollection(add);
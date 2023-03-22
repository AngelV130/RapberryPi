from sensor import Sensor
from demo_mongodb_test import ConexionMongo
import datetime
from myjson import Json

class Menu:
    def __init__(self) -> None:
        pass
    def interfaze(self):
        print("\n-----Menu-----")
        op =  input("a) Insertar Sensor\nb)Leer datos\nc)Subir Datos\nd)Leer Sensores\ne)Recargar Sensores\n Elige una opcion: ")
        if(op == "a"):
            self.insertarSensor()
        elif(op=="b"):
            self.leerDatos()
        elif(op=="c"):
            self.subirDatos()
        elif(op=='d'):
            Sensor.mostrarSensores()
        elif(op == 'e'):
            self.cargarSensores()
        else:
            print("opcion no valida")
    def insertarSensor(self):
        id = input("Edcribir id: ")
        nombre = input("Escribir nombre: ");
        tipo = self._tipoSensor();
        op = 's'
        cont = 0;
        pines=[]
        while (op != 'n'):
            pines.append(int(input("Escribir el pin: ")))
            op = input("Desea agregar el otro pin s/n: ")
            cont = cont + 1;
            if cont == 2:
                break;
            if op != 's':
                break;
        ubicacion = input("Escribir ubicacion: ")
        descripcion = input("Escribir descripcion: ")
        fecha = str(datetime.datetime.now())
        sensor = Sensor(id,nombre,tipo,ubicacion,descripcion,fecha,pines)
        conexion = ConexionMongo("Sensores","senosresInfo");
        conexion.agregarCollection(sensor.__dict__)
        conexion.cerrarConexion()
        Sensor.guardarSensores()
    def _tipoSensor(self):
        op = input("---SENSORES---\n1)Corriente\n2)Sonido\n3)Flama\n4)Luz\n5)Humo\n6)Presencia\n7)Temperatura\n8)Magnetico\n9)Humedad\nElige un tipo: ")
        if op == "1":
            return "corriente"
        elif op == "2":
            return "sonido"
        elif op == "3":
            return "flama"
        elif op == "4":
            return "luz"
        elif op == "5":
            return "humo"
        elif op == "6":
           return  "presencia"
        elif op == "7":
            return "temperatura"
        elif op == "8":
            return "magnetico"
        elif op == '9':
            return "ultrasonico"
        else:
            print("Esa opcion no existe ")
            return self._tipoSensor()
    def leerDatos(self):
        Sensor.mandarDatos()
        Sensor.leerSensor()
    def subirDatos(self):
        Sensor.mandarDatos(15);
    def cargarSensores(self):
        json = Json('sensores.json')
        conexion = ConexionMongo("Sensores","senosresInfo")
        json.guardar(conexion.traerDatos())

if __name__ == '__main__':
    menu = Menu()
    while True:
        menu.interfaze()
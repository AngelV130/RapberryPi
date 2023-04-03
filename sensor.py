from lista import Lista
from demo_mongodb_test import ConexionMongo
from datetime import datetime
from myjson import Json
import serial
import time
import RPi.GPIO as GPIO
import Adafruit_DHT

class Sensor:
    def __init__(self,_id,nombre,tipo,ubicacion,descripcion,fecha_creacion,pines) :
        self._id = _id
        self.nombre = nombre
        self.tipo = tipo
        self.pines = pines
        self.ubicacion = ubicacion
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
    @staticmethod
    
    def leerSensor():
        json = Json('sensores.json')
        sensores = json.cargar()
        if len(sensores) < 1:
            return print("no hay sensores para leer")
        cont = 0;
        lista = Lista("sensoresData.json")
        dataLocal = lista.cargar()
        if dataLocal != []:
            for dato in dataLocal:
                lista.agregar(dato);
        puerto_serial = serial.Serial('/dev/tty*', 9600)
        while True:
            if sensores[cont]['tipo'] == 'temperatura y humedad':
                Sensor.leerRaspberryPi(sensores[cont]);
                count = count + 1
            else:    
                #Arduino ejemplo
                data = puerto_serial.readline().decode('utf-8').rstrip();
                data2 = data.split(":")
                if(len(data2) >= 3):
                    sensorData = {"type":data2[0],"values":[data2[1],data2[2]],"fecha_creacion":str(datetime.now()),"sensor":sensores[cont]}
                else:
                    sensorData = {"type":data2[0],"value":data2[1],"fecha_creacion":str(datetime.now()),"sensor":sensores[cont]}
                if data2[0] == sensores[cont]['tipo']:
                    lista.agregar(sensorData)
                    cont+=1
            print("Vuelta ",cont)
            if(cont == len(sensores)):
                lista.guardar(lista.lista)
                op = input("Dese leer nuevamente los sensores? ('si','no' O 's','n')    ")
                if op == 'no' or op == 'n':
                    break;
                elif op == 'si' or op == 's':
                    cont = 0;
                else:
                    print('Opcion no detectada!....')
                    break;
    @staticmethod   
    def mandarDatos(diferencia_en_minutos = 0):
        datos = Json('sensoresData.json')
        if datos.cargar() != []:
            # leer tiempo
            fecha_actual = datetime.now()
            ultima_fecha = datos.cargar()[-1]['fecha_creacion']
            # Calcular la diferencia en minutos
            if diferencia_en_minutos < 15:
                diferencia_en_minutos = (fecha_actual - datetime.strptime(ultima_fecha, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() // 60
            if diferencia_en_minutos >= 15.0:
                conexion = ConexionMongo("Sensores","sensoresDatos")
                if conexion.verificacion:
                    if datos.cargar('sensoresDatRespaldo.json') != []:
                        conexion.agregarCollection(datos.cargar('sensoresDatRespaldo.json'))
                        datos.limpiar('sensoresDatRespaldo.json');
                    conexion.agregarCollection(datos.cargar())
                    datos.limpiar('sensoresData.json');
                    conexion.cerrarConexion()
                else:
                    datos.guardar(datos.cargar(),'sensoresDatRespaldo.json')
                    datos.limpiar('sensoresData.json');
            else:
                print(diferencia_en_minutos)
                print("No se subieron datos")
        else:
            print("no hay datos que mandar")
    @staticmethod
    def mostrarSensores():
        file = Json('sensores.json');
        sensores =file.cargar();
        if sensores != []:
            print("Nombre\t\tTipo\t\tUbicacion\tDescripcion\t\tFecha")
            for sensor in sensores:
                print(f"{sensor['nombre']}\t{sensor['tipo']}\t{sensor['ubicacion']}\t{sensor['descripcion']}\t\t{sensor['fecha_creacion']}\t")
        else:
            print("No hay sensores")
    @staticmethod
    def guardarSensores():
        file = Json('sensores.json');
        conexion = ConexionMongo('Sensores','senosresInfo')
        file.guardar(conexion.traerDatos())
    @staticmethod
    
    def leerRaspberryPi(sensor):
        lista = Lista("sensoresData.json")
        dataLocal = lista.cargar()
        if dataLocal != []:
            for dato in dataLocal:
                lista.agregar(dato);
        if sensor['tipo'] == "temperatura y humedad":
            while True:
                dht = Adafruit_DHT.DHT11 #Cambia por DHT22 y si usas dicho sensor
                humedad, temperatura = Adafruit_DHT.read_retry(dht, sensor['pines'][0])
                print ('Humedad: ' , format(humedad))
                print ('Temperatura: ' , format(temperatura))
                sensorData = {"type":'temperatura',"value":temperatura,"fecha_creacion":str(datetime.now()),"sensor":sensor}
                sensorData2 = {"type":'humedad',"value":humedad,"fecha_creacion":str(datetime.now()),"sensor":sensor}
                lista.agregar(sensorData)
                lista.agregar(sensorData2)
                break; #Cada segundo se evalúa el sensor
        lista.guardar(lista.lista);
    @staticmethod
    def led():
        pin = 12
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(pin, GPIO.LOW)
        res = ""
        while res != "si":
            print("1-Apagar led")
            print("2-Encender led")
            opcion = input("Que deseas hacer?")
            try:
                opcion = int (opcion)
            except:
                print("eso no es un numero")
            if opcion == 1:
                GPIO.output(pin, GPIO.LOW)
            elif opcion == 2:
                GPIO.output(pin, GPIO.HIGH)
            else:
                print("Opcion no valida")
            res = input("deseas salir?")
        GPIO.cleanup()


#Sensor.mostrarSensores()
#input("escribe algo")



#serial
# Configura el objeto Serial
#puerto_serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Lee datos del puerto serial
#while True:
    #linea = puerto_serial.readline().decode('utf-8').rstrip()
    #if linea:
        #print(linea)
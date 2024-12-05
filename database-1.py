from flask import flash
import pymysql

class Database:
    def __init__(self, host="localhost", user="root", password="", database="registroautos"):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def insert_data(self, placa, confirm_placa, serie, confirm_serie, modelo, correo_electronico, fecha_cita):
        query = """
        INSERT INTO registros (Placa, Confirmar_Placa, Serie, Confirmar_Serie, Modelo, Correo_Electronico, Fecha_Cita)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (placa, confirm_placa, serie, confirm_serie, modelo, correo_electronico, fecha_cita))
        self.connection.commit()

from flask import Flask, request, render_template, redirect, url_for
import psycopg2
from config import conectar, desconectar
import os

app = Flask(__name__)


@app.route("/ProyectoSENA")
def index():
    return render_template("index.html")
    
@app.route("/ProyectoSENA/registrar", methods=["GET", "POST"])
def registrar():
    if request.method=="POST":
        identificacion = request.form ["identificacion"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        telefono = request.form["telefono"]
        cargo = request.form["cargo"]
        salario = request.form ["salario"]
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            consulta = """
            INSERT INTO empleados (identificacion, nombre, apellido, telefono, cargo, salario)
            VALUES (%S, %S, %S, %S, %S, %S)
            """	
            datos = (identificacion, nombre, apellido, telefono, cargo, salario)
            cursor.execute(consulta, datos)
            conexion.commit()
            print("Empleado registrado exitosamente")
            return "El empleado fue registrado con éxito!"
        except (Exception, psycopg2.Error) as error:
            print("Error al registrar el empleado:", error)
            return "Error al registrar el empleado"
        finally:
            if conexion:
                desconectar(conexion)
                cursor.close()
    else:
        return render_template("registrar.html")
    
@app.route("/ProyectoSENA/consultar", methods=["GET"])
def consultar():
    conexion = conectar()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM empleados"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    desconectar(conexion)
    return render_template("consultar.html", datos=datos)

@app.route("/ProyectoSENA/actualizar_empleado", methods=["POST"])
def actualizar_empleado():
    id = request.form["id"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    telefono = request.form["telefono"]
    cargo = request.form["cargo"]
    salario = request.form["sañario"]
    try: 
        conexion = conectar()
        cursor = conexion.cursor()
        consultar = """
        UPDATE compleados SET
        nombre = %S, apellido =%S, telefono = %S, cargo = %S, salario = %S
        WHERE id = %S;
        """

        datos = (nombre, apellido, telefono, cargo, salario, id)
        cursor.execute(consultar, datos)
        conexion.commit()
        return "El empleado fue actualizado con éxito!"
    except (Exception, psycopg2.Error) as error:
        return "Error al actualizar el empleo", error
    finally:
        if conexion:
            desconectar(conexion)
            cursor.close()
    
@app.route("/ProyectoSENA/eliminar", methods=["GET","POST"])
def eliminar():
    if request.method == "POST":
        doc = request.form["ident"]
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cosultar = """ DELETE FROM emleado WHERE identificacion = %S """
            datos=(doc,)
            cursor.execute(consultar, datos)
            conexion.close()
            return "El empleado fue eliminado el empleado correctamente!"
        except (Exception, psycopg2.Error) as error:
            return "Error al eliminar el empleado ",error
        finally:
            if conexion:
                desconectar(conexion)
                cursor.close()
    else: 
        return render_template("eliminar.html")


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template, redirect, url_for
import psycopg2
from config import conectar, desconectar
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        identificacion = request.form["identificacion"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        telefono = request.form["telefono"]
        cargo = request.form["cargo"]
        salario = request.form["salario"]
        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute("SELECT id FROM empleados WHERE identificacion = %s", (identificacion,))
            if cursor.fetchone():
                return "Ya existe un empleado registrado con esa identificación."

            sql = """
            INSERT INTO empleados (identificacion, nombre, apellido, telefono, cargo, salario)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            datos = (identificacion, nombre, apellido, telefono, cargo, salario)
            cursor.execute(sql, datos)
            conexion.commit()
            return "El empleado fue registrado con éxito!"
        except (Exception, psycopg2.Error) as error:
            return f"Error al registrar el empleado: {error}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                desconectar(conexion)
    else:
        return render_template("registrar.html")

@app.route("/consultar", methods=["GET"])
def consultar():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "SELECT * FROM empleados"
    cursor.execute(sql)
    datos = cursor.fetchall()
    cursor.close()
    desconectar(conexion)
    return render_template("consultar.html", datos=datos)

@app.route("/actualizar_empleado", methods=["POST"])
def actualizar_empleado():
    id = request.form["id"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    telefono = request.form["telefono"]
    cargo = request.form["cargo"]
    salario = request.form["salario"]
    conexion = None
    cursor = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
        UPDATE empleados SET
        nombre = %s, apellido = %s, telefono = %s, cargo = %s, salario = %s
        WHERE id = %s;
        """
        datos = (nombre, apellido, telefono, cargo, salario, id)
        cursor.execute(sql, datos)
        conexion.commit()
        return "El empleado fue actualizado con éxito!"
    except (Exception, psycopg2.Error) as error:
        return f"Error al actualizar el empleado: {error}"
    finally:
        if cursor:
            cursor.close()
        if conexion:
            desconectar(conexion)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    if request.method == "POST":
        doc = request.form["ident"]
        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "DELETE FROM empleados WHERE identificacion = %s"
            datos = (doc,)
            cursor.execute(sql, datos)
            conexion.commit()
            return "El empleado fue eliminado correctamente!"
        except (Exception, psycopg2.Error) as error:
            return f"Error al eliminar el empleado: {error}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                desconectar(conexion)
    else:
        return render_template("eliminar.html")

if __name__ == '__main__':
    app.run(debug=True)
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

from django.http import HttpResponseRedirect
from django.urls import reverse


from . import forms

from .models import Curso

import sqlite3

import requests


def index(request):
    return HttpResponse("¡Hola, mundo!")


def acerca_de(request):
    return HttpResponse("¡Curso de Python y Django!")


def cursos(request):
    conn = sqlite3.connect("cursos.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM cursos")
    html = """
    <html>
    <title>Lista de cursos</title>
    <table style="border: 1px solid">
    <thead>
    <tr>
    <th>Curso</th>
    <th>Inscriptos</th>
    </tr>
    </thead>
    """
    for (nombre, inscriptos) in cursor.fetchall():
        html += f"""
        <tr>
        <td>{nombre}</td>
        <td>{inscriptos}</td>
        </tr>
        """
    html += "</table></html>"
    conn.close()
    return HttpResponse(html)


def servicio(request):
    conn = sqlite3.connect("cursos.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM cursos")
    response = JsonResponse(cursor.fetchall(), safe=False)
    conn.close()
    return response


def nuevo_index(request):
    """
    ctx = {
        "nombre": "Juan",
        "cursos": 5,
        "curso_actual": "Python & Django"
    }
    """
    return render(request, "index.html")


def dolar(request):
    # return JsonResponse({"clave": "valor"}, safe=False)
    r = requests.get(
        "https://api-dolar-argentina.herokuapp.com/api/dolaroficial")
    oficial = r.json()
    r = requests.get("https://api-dolar-argentina.herokuapp.com/api/dolarblue")
    blue = r.json()
    precios = {"oficial": oficial, "blue": blue}
    response = JsonResponse(precios, safe=False)
    return response


def dolar_vista(request):
    # return JsonResponse({"clave": "valor"}, safe=False)
    r = requests.get(
        "https://api-dolar-argentina.herokuapp.com/api/dolaroficial")
    oficial = r.json()
    r = requests.get("https://api-dolar-argentina.herokuapp.com/api/dolarblue")
    blue = r.json()
    precios = {"oficial": oficial, "blue": blue}
    texto = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dolar</title>
    </head>
    <body>
    <h1>Dolar</h1> <br>
    <p><b>Oficial</b></p> <br>
    <p><b>Compra:</b>{oficial["compra"]} </p>
    <p><b>Venta:</b>{oficial["venta"]} </p> <br> <br>
    <p><b>Blue</b></p> <br>
    <p><b>Compra:</b>{blue["compra"]} </p>
    <p><b>Venta:</b>{blue["venta"]} </p> <br>
    </body>
    </html>
    """
    return HttpResponse(texto)


def dolar_render(request):
    # return JsonResponse({"clave": "valor"}, safe=False)
    r = requests.get(
        "https://api-dolar-argentina.herokuapp.com/api/dolaroficial")
    oficial = r.json()
    r = requests.get("https://api-dolar-argentina.herokuapp.com/api/dolarblue")
    blue = r.json()
    ctx = {"oficial": oficial, "blue": blue}
    return render(request, "dolarv.html", ctx)


def aeropuertos(request):
    f = open("aeropuertos.csv", encoding="utf8")
    datos = f.readlines()
    f.close()
    renglon = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dolar</title>
    </head>
    <body>
    <table border="1">
    <tr>
    <th>Aeropuerto</th>
    <th>Ciudad</th>
    <th>Pais</th>
    <\tr>
    """
    for n in datos:
        aux = n.split(",")
        aeropuerto = aux[1].replace('"', "")
        ciudad = aux[2].replace('"', "")
        pais = aux[3].replace('"', "")
        renglon += f"<tr> <td>{aeropuerto}</td> <td>{ciudad}</td>  <td>{pais}</td> </tr>"
    renglon += """
    </table>
    </body>
    </html>
    """
    return HttpResponse(renglon)


def cursos_render(request):
    conn = sqlite3.connect("cursos.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM cursos")
    cursos = cursor.fetchall()
    conn.close()
    ctx = {"cursos": cursos}
    return render(request, "cursos.html", ctx)


def curso(request, nombre_curso):
    conn = sqlite3.connect("cursos.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, inscriptos FROM cursos WHERE nombre=?", [nombre_curso])
    curso = cursor.fetchone()
    ctx = {"curso": curso}
    conn.close()
    return render(request, "curso.html", ctx)


def nuevo_curso(request):
    if request.method == "POST":
        form = forms.FormularioCurso(request.POST)
        if form.is_valid():
            conn = sqlite3.connect("cursos.sqlite3")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cursos VALUES (?, ?)",
                           (form.cleaned_data["nombre"], form.cleaned_data["inscriptos"]))
            conn.commit()
            conn.close()
            return HttpResponseRedirect(reverse("cursos_render"))
    else:
        form = forms.FormularioCurso()
        ctx = {"form": form}
        return render(request, "nuevo_curso.html", ctx)


def modelos(request):
    cursos = Curso.objects.all()
    total = 0
    for n in cursos:
        total = total + n.inscriptos
    ctx = {"cursos": cursos,"inscriptos":total}
    return render(request, "modelos.html", ctx)


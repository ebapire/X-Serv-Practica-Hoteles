# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import Hotel, Imagen, Comentario, Hotel_selecc, CSS, Titulo
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import parse
import urllib2
import random
import datetime
from django.contrib.auth.models import User


# Create your views here.


def parsear (idioma):
    if idioma =='es':
        xmlfile = urllib2.urlopen("http://www.esmadrid.com/opendata/alojamientos_v1_es.xml")
    elif idioma =='en':
        xmlfile = urllib2.urlopen("http://www.esmadrid.com/opendata/alojamientos_v1_en.xml")
    elif idioma =='fr':
        xmlfile = urllib2.urlopen("http://www.esmadrid.com/opendata/alojamientos_v1_fr.xml")

    theParser = make_parser()
    theHandler = parse.myContentHandler()
    theParser.setContentHandler(theHandler)
    theParser.parse(xmlfile)
    hoteles = theHandler.terminar()
    return hoteles

def hoteles_mas_comms ():
    hotels = Hotel.objects.order_by('-tot_comentarios')
    lista_hoteles = "<ul>"
    hotel = []
    i = 0
    for hotel in hotels:
        if hotel.tot_comentarios > 0:
            lista_hoteles += "<p><li><a href='" + hotel.Url + "'>"+ hotel.Nombre + "</a> Direccion: " + hotel.Direccion
            lista_hoteles += "<br><a href='alojamiento/" + str(hotel.id) + "'> Mas Informacion</a>"
            try:
                lista_imagenes = Imagen.objects.filter(Hotel_id=hotel)
                if (len(lista_imagenes) > 0):
                    lista_hoteles += "<br><img class='imagenPeq' src='" + lista_imagenes[0].Url + "'>"
            except Imagen.DoesNotExist:
                pass
        i = i+1
        if i == 10:
            break

    lista_hoteles += "</ul>"
    return lista_hoteles

def pags_personales():
    users = User.objects.all()
    lista_paginas = "<ul class = sidebar>"
    if users:
        for user in users:
            try:
                titulo = Titulo.objects.get(User = user)
                tit = titulo.body
            except Titulo.DoesNotExist:
                tit = "Pagina de " + str(user.username)
            lista_paginas += "<li><a href='/" + str(user.id) + "'>" +  tit + '</a>'
    lista_paginas += "</ul>"
    return lista_paginas

def hoteles_selec (usuario):
    lista_hoteles = "<ul>"
    success = True;
    try:
        hoteles_fav = Hotel_selecc.objects.filter(User = usuario.username)
    except Hotel_selecc.DoesNotExist:
        lista_hoteles = "Este usuario no tiene ningun hotel favorito"
        success = False
        return (lista_hoteles, success)
    for hotel_fav in hoteles_fav:
        lista_hoteles += "<li><a href='/alojamiento/" + str(hotel_fav.Hotel_id.id) +\
            "'>" + hotel_fav.Hotel_id.Nombre + '</a>'
        lista_hoteles += ' Fecha de seleccion: ' + str(hotel_fav.Date)
    lista_hoteles += "</ul>"
    return (lista_hoteles, success)

def todos_hoteles():
    success = True
    try:
        hoteles = Hotel.objects.order_by("Nombre")
    except Hotel.DoesNotExist:
        lista_hoteles = "No hay alojamientos que mostar"
        success = False
        return (lista_hoteles, success)
    lista_hoteles = "<ul>"
    for hotel in hoteles:
        lista_hoteles += "<li><a href='alojamiento/" + str(hotel.id) +\
            "'>" + hotel.Nombre + '</a>'
    lista_hoteles += "</ul>"
    return (lista_hoteles, success)

def filtrar_hoteles (Categoria, Subcategoria):
    success = True
    try:
        hoteles = Hotel.objects.order_by("Nombre").filter(Categ = Categoria,
        SubCateg = Subcategoria)
    except Hotel.DoesNotExist:
        lista_hoteles = ""
        success = False;
        return (lista_hoteles, success)
    if not hoteles:
        lista_hoteles = "No hay alojamientos con esas especificaciones"
        return (lista_hoteles, success)
    lista_hoteles = "<ul>"
    for hotel in hoteles:
        lista_hoteles += "<li><a href='alojamiento/" + str(hotel.id) +\
            "'>" + hotel.Nombre + '</a>'
    lista_hoteles += "</ul>"
    return (lista_hoteles, success)

def hotel_completo (id):
    success = True
    lista_hotel = ""
    lista_imagenes = ""
    lista_cmm = ""
    try:
        hotel = Hotel.objects.get(id = id)
        comentarios = Comentario.objects.filter(Hotel_id = hotel)
        images = Imagen.objects.filter(Hotel_id = hotel)
    except (Hotel.DoesNotExist, Comentario.DoesNotExist, Imagen.DoesNotExist):
        success = False
        return (lista_hotel, lista_cmm, lista_imagenes, success)

    lista_hotel = "<b>" + hotel.Nombre + "</b><p>" + hotel.SubCateg +\
        "<br>Telefono: " + hotel.telefono + "<br>Direccion: " + hotel.Direccion +\
        ", " + hotel.zipcode + ", (" + hotel.latitude + "," + hotel.longitude + ")" +\
        "<br><a href=" + str(hotel.Url) + "'> Web </a><br>" + hotel.Descrip

    if comentarios:
        for comentario in comentarios:
            lista_cmm += "<li>" + comentario.User + ": " + comentario.body
    if images:
        i = 0
        for image in images:
            lista_imagenes +=  "<br><img src='" + image.Url + "'>"
            i = i+1
            if i == 5:
                break
    return (lista_hotel, lista_cmm, lista_imagenes, success)

def comprobar_auten (request):
    if request.user.is_authenticated():
        return (True, request.user.username)
    else:
        return (False, "")

def xml (user):
    hoteles_fav = Hotel_selecc.objects.filter(User = user.username)
    lista_xml = '<?xml version="1.0" encoding="UTF-8"?>'
    if hoteles_fav:
        lista_xml += "<ServiceList>"
        for h in hoteles_fav:
            lista_xml += "<service><basicData><name>" + h.Hotel_id.Nombre + "</name><phone>" +\
            h.Hotel_id.telefono + "</phone><web>" + h.Hotel_id.Url + "</web>" +\
            "<body><![CDATA[" + h.Hotel_id.Descrip + "]]></body></basicData>" +\
            "<geodata><address>" + h.Hotel_id.Direccion + "</address></geodata>" +\
            "<extradata><categoria>" + h.Hotel_id.Categ + "</categoria><subcategoria>" +\
            h.Hotel_id.SubCateg + "</subcategoria></extradata>"+\
            "<multimedia>"
            imagenes = Imagen.objects.filter(Hotel_id = h.Hotel_id)
            for imagen in imagenes:
                lista_xml += "<url>"+ imagen.Url + "</url>"
            lista_xml += "</multimedia></service>"

        lista_xml += "</ServiceList>"
    return lista_xml

def comprobar_css (user):
    letra = "100%"
    color = "white"
    try:
        css = CSS.objects.get(User= user)
        letra = css.Letra
        color = css.Color
    except CSS.DoesNotExist:
        pass;
    return (letra, color)

#-----------urls.py
def principal (request):
    hotels = Hotel.objects.all()
    hoteles = []
    if not hotels:
        hoteles = parsear('es')
        for hotel in hoteles:
            try:
                new_hotel = Hotel(Nombre = hotel["name"],
                Categ = hotel["Categoria"], Descrip = hotel["body"],
                Direccion = hotel["address"], Url = hotel["web"],
                telefono = hotel["phone"], SubCateg = hotel["SubCategoria"],
                latitude = hotel["latitude"], longitude = hotel["longitude"],
                zipcode = hotel["zipcode"])
            except KeyError:
                continue
            new_hotel.save()
            try:
                for url in hotel["url"]:
                    new_image = Imagen(Url = url, Hotel_id = new_hotel)
                    new_image.save()
            except KeyError:
                continue

    lista_hoteles = hoteles_mas_comms()
    lista_paginas = pags_personales()


    (is_authenticated, user) = comprobar_auten(request)
    if is_authenticated:
        (letra, color) = comprobar_css(user)
        template = loader.get_template("principal.html")
        contexto = {'content': lista_hoteles, 'sidebar': lista_paginas, 'letra': letra, 'color': color}
    else:
        template = loader.get_template("principal_anonima.html")
        contexto = {'content': lista_hoteles, 'sidebar': lista_paginas}
    return HttpResponse(template.render(Context(contexto)))

@csrf_exempt
def anadir_css (request):
    (is_authenticated, user) = comprobar_auten(request)
    user = User.objects.get(username = user)
    letra = request.POST['Letra']
    color = request.POST['Color']
    if letra == "Elige un tamaño de letra" or color == "Elige un color de fondo":
        pass
    else:
        try:
            css = CSS.objects.get(User= user.username)
            css.Letra = letra
            css.Color = color
            css.save()
        except CSS.DoesNotExist:
            new_css = CSS(User = user, Letra = letra, Color = color)
            new_css.save()
    return HttpResponseRedirect("http://localhost:8000/usuario/" + str(user.id))

@csrf_exempt
def usuario (request, iduser):
    user = request.user
    lista_hotel = ""
    if request.method == 'POST':
        titulo = request.POST['titulo']
        try:
            tit_aux = Titulo.objects.get(User = user)
            tit_aux.body = titulo
            tit_aux.save()
        except Titulo.DoesNotExist:
            new_tit = Titulo(User = user, body = titulo)
            new_tit.save()
        return HttpResponseRedirect("")
    elif request.method == 'GET':
        try:
            user = User.objects.get(id = iduser)
        except User.DoesNotExist:
            title = "Error"
            template = loader.get_template("404.html")
            contexto = {'content': "Usuario no registrado"}
            return HttpResponse(template.render(Context(contexto)))
        try:
            title = Titulo.objects.get(User = user.username)
            title = title.body
        except Titulo.DoesNotExist:
            title = "Pagina personal de " + str(user.username)
        (lista_hoteles, success) = hoteles_selec(user)
        if success == False:
            title = "Error"
            template = loader.get_template("404.html")
            contexto = {'content': "Usuario no registrado"}
            return HttpResponse(template.render(Context(contexto)))

        (is_authenticated, user) = comprobar_auten(request)

        path = "" + iduser + "/xml"
        if is_authenticated:
            (letra, color) = comprobar_css(user)
            template = loader.get_template("usuario.html")
            contexto = {'content': lista_hoteles, 'title': title, 'letra': letra, 'color': color, 'path': path}
        else:
            template = loader.get_template("usuario_anonimo.html")
            contexto = {'content': lista_hoteles, 'title': title, 'path': path}
    else:
        template = loader.get_template("404.html")
        contexto = {'content': "Metodo no permitido"}
        return HttpResponse(template.render(Context(contexto)))
    return HttpResponse(template.render(Context(contexto)))

def alojamientos (request):
    (lista_hoteles, success) = todos_hoteles()
    if success == False:
        title = "Error"
        template = loader.get_template("404.html")
        contexto = {'content': "No hay hoteles que mostrar"}
        return HttpResponse(template.render(Context(contexto)))

    (is_authenticated, user) = comprobar_auten(request)
    if is_authenticated:
        (letra, color) = comprobar_css(user)
        contexto = {'content': lista_hoteles,'letra': letra, 'color': color}
        template = loader.get_template("alojamientos.html")
    else:
        template = loader.get_template("alojamientos_anonima.html")
        contexto = {'content': lista_hoteles}
    return HttpResponse(template.render(Context(contexto)))

@csrf_exempt
def idioma(request, id_aloj):
    (lista_hotel, lista_cmm, lista_imagenes, success) = hotel_completo(id_aloj)
    hotel = Hotel.objects.get(id = id_aloj)
    idioma = request.POST['Idioma']
    if idioma != "Need other language?":
        hoteles = parsear(idioma)
        for h in hoteles:
            if h["name"] == hotel.Nombre:
                lista_hotel += "<br>" + h["body"]
        path = "/alojamiento/" + id_aloj + "/idioma"
        template = loader.get_template("alojamiento.html")
        (is_authenticated, user) = comprobar_auten(request)
        if is_authenticated:
            (letra, color) = comprobar_css(user)
            template = loader.get_template("alojamientos.html")
            contexto = {'content': lista_hotel+lista_cmm+lista_imagenes, 'path': path,'letra': letra, 'color': color}
        else:
            contexto = {'content': lista_hotel+lista_cmm+lista_imagenes, 'path': path}
        return HttpResponse(template.render(Context(contexto)))


@csrf_exempt
def alojamiento(request, id_aloj):
    success = True;
    if request.method == 'POST':
        (is_authenticated, user) = comprobar_auten(request)
        hotel = Hotel.objects.get(id = id_aloj)
        if is_authenticated:
            try:
                comm = request.POST['comentarios']
                now = datetime.datetime.now()
                Comentario_aux = Comentario.objects.filter(Hotel_id = hotel, User = user)
                if not Comentario_aux:
                    new = Comentario(User = user, body = comm, Date = now, Hotel_id = hotel)
                    hotel.tot_comentarios = hotel.tot_comentarios +1
                    hotel.save()
                    new.save()
            except:
                try:
                    h_aux = Hotel_selecc.objects.get(User = user, Hotel_id = hotel)
                except Hotel_selecc.DoesNotExist:
                    now = datetime.datetime.now()
                    new_htl_selec = Hotel_selecc(User = user, Date = now, Hotel_id = hotel)
                    new_htl_selec.save()
            return HttpResponseRedirect("")
    elif request.method == 'GET':
        (is_authenticated, user) = comprobar_auten(request)
        (lista_hotel, lista_cmm, lista_imagenes, success) = hotel_completo(id_aloj)
        if is_authenticated:
            (letra, color) = comprobar_css(user)
            path = "/alojamiento/" + id_aloj + "/idioma"
            template = loader.get_template("alojamiento.html")
            contexto = {'content': lista_hotel+lista_cmm+lista_imagenes, 'path': path, 'letra': letra, 'color': color}
        else:
            template = loader.get_template("alojamiento_anonima.html")
            contexto = {'content': lista_hotel+lista_cmm+lista_imagenes}
        return HttpResponse(template.render(Context(contexto)))
    else:
        template = loader.get_template("404.html")
        contexto = {'content': "Metodo no permitido"}
        return HttpResponse(template.render(Context(contexto)))

def about(request):
    template = loader.get_template("about.html")
    return HttpResponse(template.render(Context()))

@csrf_exempt
def hoteles_filt(request):
    (is_authenticated, user) = comprobar_auten(request)
    if request.method == 'POST':
        Subcategoria = request.POST['SubCateg']
        Categoria = request.POST['Categ']
        (lista_hoteles, success) = filtrar_hoteles(Categoria, Subcategoria)
        if success == False:
            template = loader.get_template("404.html")
            contexto = {'content': "No hay hoteles que mostrar"}
            return HttpResponse(template.render(Context(contexto)))
        template = loader.get_template("filter.html")
        if is_authenticated:
            (letra, color) = comprobar_css(user)
            contexto = {'content': lista_hoteles, 'letra': letra, 'color': color}
        else:
            contexto = {'content': lista_hoteles}
        return HttpResponse(template.render(Context(contexto)))
    else:
        template = loader.get_template("404.html")
        contexto = {'content': "Metodo no permitido"}
        return HttpResponse(template.render(Context(contexto)))

def user_xml (request, id):
    try:
        user = User.objects.get(id = id)
    except User.DoesNotExist:
        title = "Error"
        template = loader.get_template("404.html")
        contexto = {'content': "Usuario no registrado"}
        return HttpResponse(template.render(Context(contexto)))
    lista_hoteles = xml(user)
    return HttpResponse(lista_hoteles, content_type = 'xml')

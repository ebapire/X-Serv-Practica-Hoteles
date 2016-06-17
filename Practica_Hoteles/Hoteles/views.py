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

def new_hotel_aleat ():
    number_of_hotels = Hotel.objects.count()
    random_index = int(random.random()*number_of_hotels)+1
    hotel = Hotel.objects.get(id = random_index)
    return hotel

def new_comentario (text):
    hotel = new_hotel_aleat()
    now = datetime.datetime.now()
    new_comn = Comentario(User = 'eba', Date = now, body = text, Hotel_id = hotel)
    new_comn.save()
    tot_comm = hotel.tot_comentarios +1
    hotel.tot_comentarios = tot_comm
    hotel.save()


def hoteles_mas_comms ():
    hotels = Hotel.objects.order_by('-tot_comentarios')
    lista_hoteles = "<ul>"
    hotel = []
    i = 0
    for hotel in hotels:
        if hotel.tot_comentarios > 0:
            lista_hoteles += "<li><a href='" + hotel.Url + "'>"+ hotel.Nombre + "</a> Direccion: " + hotel.Direccion
            try:
                lista_imagenes = Imagen.objects.filter(Hotel_id=hotel)
                if (len(lista_imagenes) > 0):
                    lista_hoteles += "<img class='imagenPeq' src='" + lista_imagenes[0].Url + "'>"
            except Imagen.DoesNotExist:
                pass
            lista_hoteles += "<a href='alojamiento/" + str(hotel.id) + "'> Mas Informacion</a>"
        i = i+1
        if i == 10:
            break

    lista_hoteles += "</ul>"
    return lista_hoteles

def pags_personales():
    users = User.objects.all()
    lista_paginas = "<ul>"
    if users:
        for user in users:
            try:
                titulo = Titulo.objects.get(User = user)
                tit = titulo.body
            except Titulo.DoesNotExist:
                tit = "Pagina de " + str(user.username)
            lista_paginas += "<li><a href='usuario/" + str(user.id) + "'>" +  tit + '</a>'
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
    lista_cmm = ""
    lista_hotel = ""
    lista_imagenes = ""
    success = True
    try:
        hotel = Hotel.objects.get(id = id)
        comentarios = Comentario.objects.filter(Hotel_id = hotel)
        images = Imagen.objects.filter(Hotel_id = hotel)
    except (Hotel.DoesNotExist, Comentario.DoesNotExist, Imagen.DoesNotExist):
        success = False
        return (lista_hotel, lista_cmm, lista_imagenes, success)

    lista_hotel = "<b>" + hotel.Nombre + "</b><p>" + hotel.SubCateg +\
        "<br>Telefono: " + hotel.telefono + "<br>Direccion: " + hotel.Direccion +\
        "<br><a href=" + str(hotel.Url) + "'> Web </a><br>" + hotel.Descrip
    if comentarios:
        for comentario in comentarios:
            lista_cmm += "<li>" + comentario.body
    if images:
        i = 0
        for image in images:
            lista_imagenes +=  "<img class='imagenPeq' src='" + image.Url + "'>"
            i = i+1
            if i == 5:
                break
    return (lista_hotel, lista_cmm, lista_imagenes, success)

def comprobar_auten (request):
    if request.user.is_authenticated():
        return (True, request.user.username)
    else:
        return (False, null)

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
                telefono = hotel["phone"], SubCateg = hotel["SubCategoria"])
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
        template = loader.get_template("principal.html")
    else:
        template = loader.get_template("principal_anonima.html")
    contexto = {'content': lista_hoteles, 'sidebar': lista_paginas}
    return HttpResponse(template.render(Context(contexto)))

def usuario (request, iduser):
    try:
        user = User.objects.get(id = iduser)
    except User.DoesNotExist:
        title = "Error"
        template = loader.get_template("404.html")
        contexto = {'content': "Usuario no registrado"}
        return HttpResponse(template.render(Context(contexto)))
    title = "Pagina personal de " + str(user.username)
    (lista_hoteles, success) = hoteles_selec(user)
    if success == False:
        title = "Error"
        template = loader.get_template("404.html")
        contexto = {'content': "Usuario no registrado"}
        return HttpResponse(template.render(Context(contexto)))
    template = loader.get_template("usuario.html")
    contexto = {'content': lista_hoteles, 'title': title}
    return HttpResponse(template.render(Context(contexto)))

def alojamientos (request):
    (lista_hoteles, success) = todos_hoteles()
    if success == False:
        title = "Error"
        template = loader.get_template("404.html")
        contexto = {'content': "No hay hoteles que mostrar"}
        return HttpResponse(template.render(Context(contexto)))
    template = loader.get_template("alojamientos.html")
    contexto = {'content': lista_hoteles}
    return HttpResponse(template.render(Context(contexto)))

@csrf_exempt
def alojamiento(request, id_aloj):
    if request.method == 'POST':
        comm = request.POST['comentarios']
        now = datetime.datetime.now()
        hotel = Hotel.objects.get(id = id_aloj)
        new = Comentario(body = comm, Date = now, Hotel_id = hotel)
        new.save()
        return HttpResponseRedirect("")
    elif request.method == 'GET':
        (is_authenticated, user) = comprobar_auten(request)
        if is_authenticated:
            template = loader.get_template("alojamiento.html")
        else:
            template = loader.get_template("alojamiento_anonima.html")

        (lista_hotel, lista_cmm, lista_imagenes, success) = hotel_completo(id_aloj)
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
    if request.method == 'POST':
        Subcategoria = request.POST['SubCateg']
        Categoria = request.POST['Categ']
        (lista_hoteles, success) = filtrar_hoteles(Categoria, Subcategoria)
        if success == False:
            template = loader.get_template("404.html")
            contexto = {'content': "No hay hoteles que mostrar"}
            return HttpResponse(template.render(Context(contexto)))
        template = loader.get_template("filter.html")
        contexto = {'content': lista_hoteles}
        return HttpResponse(template.render(Context(contexto)))
    else:
        template = loader.get_template("404.html")
        contexto = {'content': "Metodo no permitido"}
        return HttpResponse(template.render(Context(contexto)))

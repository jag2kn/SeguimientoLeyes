# coding: utf-8
from django.http import HttpResponse
import json
import datatables

from models import *


def listaPonentes(ponentes):
	lista = []
	for p in ponentes:
		ponente = {"nombre": p.nombre, "partido": p.partido.nombre}
		lista.append(ponente)
	return lista
		
def listaArticulos(articulos):
	lista = []
	for a in articulos:
		obs = Observaciones.objects.filter(articulo=a)
		observaciones = []
		for o in obs:
			observaciones.append({"texto":o.texto, "autor":o.autor.username})
		articulo = {"nombre": a.nombre, "texto":a.texto, "observaciones":observaciones}
		lista.append(articulo)
	return lista


def detalle(request, proyecto_id):
	proyecto = Proyecto.objects.get(id=proyecto_id)
	ponentes = Senador.objects.filter(proyecto=proyecto)
	articulos = Articulo.objects.filter(proyecto=proyecto)
	response_data = {
		"st": "success",
		"data": {
				"id": proyecto.id,
				"numero": proyecto.numero,
				"nombre": proyecto.nombre,
				"fechaRadicacion": proyecto.fechaRadicacion.strftime("%Y-%m-%d %H:%M"),
				"descripcion": proyecto.descripcion,
				"estado": str(proyecto.estado),
				"ponentes": listaPonentes(ponentes),
				"articulos": listaArticulos(articulos)
			}
	}
	return HttpResponse(json.dumps(response_data),
						mimetype="application/json")	



def ajusteColumnaPonentes(columna, ponentes):
	if columna == 'ponentes':
		return "Ponentes: "+str(ponentes)
	return ponentes


def lista(request):

	aColumns = ['id', 'numero', 'nombre', 'fechaRadicacion', 'estado', 'ponentes']
	aColumnsType = ['', 'str', 'str', 'date', 'object', '']
	sTable = "Proyecto"
	sIndexColumn = "id"

	return datatables.consulta(request, sTable, sIndexColumn, aColumns,
								aColumnsType, ajusteColumnaPonentes)



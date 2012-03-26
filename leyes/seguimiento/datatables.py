from django.http import HttpResponse
from django.db.models import Q
import json

from models import *
from mongoengine.django.auth import User


def consulta(request, sTable, sIndexColumn, aColumns, aColumnsType, callback=None):
	# Array of database columns which should be read and sent back to DataTables. Use a space where
	# you want to insert a non-database field (for example a counter or static image)

	filtro = ""
	separador = ""

	# Paging
	sLimit = ""
	if 'iDisplayStart' in request.GET and 'iDisplayLength' in request.GET:
		if request.GET['iDisplayLength'] != '-1':
			sLimit = "[" + str(int(request.GET['iDisplayStart'])) + ":"
			sLimit += str(int(request.GET['iDisplayLength']) + int(request.GET['iDisplayStart'])) + "]"

	# Ordering
	sOrder = ""
	if 'iSortCol_0' in request.GET:
		sOrder = ".order_by("
		tmp = ""
		for i in range(int(request.GET['iSortingCols'])):
			if request.GET['bSortable_' + str(int(request.GET['iSortCol_' + str(i)]))] == "true":
				odir = ""
				if request.GET['sSortDir_' + str(i)] == "desc":
					odir = "-"
				sOrder += tmp + "'" + odir + aColumns[int(request.GET['iSortCol_' + str(i)])] + "'"
				tmp = ", "
		if sOrder == ".order_by(":
			sOrder = ""
		else:
			sOrder += ")"

	# Filtering
	# NOTE this does not match the built-in DataTables filtering which does it
	# word by word on any field. It's possible to do here, but concerned about efficiency
	# on very large tables, and MySQL's regex functionality is very limited
	sWhere = ".all()"
	if filtro != "":
		sWhere = ".filter(" + filtro + ")"
	if 'sSearch' in request.GET:
		if request.GET['sSearch'] != "":
			sWhere = ".filter("
			tmp = ""
			for i in range(len(aColumns)):
				if aColumnsType[i] == "str":
					sWhere += tmp + "Q(" + aColumns[i] + "__contains='" + request.GET['sSearch'] + "'" + separador + filtro + ")"
					tmp = "|"
				elif aColumnsType[i] == "number":
					try:
						sWhere += tmp + "Q(" + aColumns[i] + "=" + int(request.GET['sSearch']) + filtro + ")"
						tmp = "|"
					except:
						pass
			if sWhere == ".filter(":
				sWhere = ".all("
				if filtro != "":
					sWhere = ".filter(" + filtro
			sWhere += ")"

	# Individual column filtering
	'''
	for i in range(len(aColumns)):
		if request.GET.has_key('bSearchable_'+str(i)) and request.GET.has_key('sSearch_'+str(i)):
			if request.GET['bSearchable_'+i] == "true" and request.GET['sSearch_'+i] != '':
				if sWhere == "":
					sWhere = ".filter( "
				else:
					sWhere += " AND "
				sWhere += aColumns[i] + " LIKE '%" + request.GET['sSearch_'+i] + "%' "
	'''
	# SQL queries
	# Get data to display

	print "0"
	print sTable + ".objects" + sWhere + sOrder + sLimit
	rResult = eval(sTable + ".objects" + sWhere + sOrder + sLimit)
	print "1"
	iFilteredTotal = eval(sTable + ".objects" + sWhere + sOrder + ".count()")
	print "2"
	iTotal = eval(sTable + ".objects.count()")
	print "3"

	sEcho = 0
	if 'sEcho' in request.GET:
		sEcho = int(request.GET['sEcho'])

	# Output
	output = {
		"sEcho": sEcho,
		"iTotalRecords": iTotal,
		"iTotalDisplayRecords": iFilteredTotal,
		"command": sTable + ".objects" + sWhere + sOrder + sLimit,
		"aaData": []
	}
	for reg in rResult:
		row = []
		for i in range(len(aColumns)):
			if aColumns[i] != "":
				tmp = eval("reg." + aColumns[i])
				if aColumnsType[i] == "date":
					if not tmp is None:
						tmp = tmp.strftime("%Y-%m-%d %H:%M")
				elif aColumnsType[i] == "object":
					if not tmp is None:
						tmp = tmp.__unicode__()
				elif aColumnsType[i] == "id":
					if not tmp is None:
						tmp = str(tmp)
				if tmp is None:
					tmp = ""

				if not callback is None:
					tmp = callback(aColumns[i], tmp)

				row.append(tmp)
		output['aaData'].append(row)

	return HttpResponse(json.dumps(output), mimetype="application/json")

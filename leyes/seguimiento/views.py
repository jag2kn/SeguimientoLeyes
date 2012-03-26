# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *

# Create your views here.
def home(request):
	return render_to_response(
				'index.html',
				context_instance=RequestContext(request))



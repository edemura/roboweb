#!C:\roboweb\winenv\bin\python
import wsgiref.handlers

from robo7tools.wsgi import application

wsgiref.handlers.CGIHandler().run(application)

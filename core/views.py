from django.shortcuts import render
from django.views.generic import TemplateView


class TeamView(TemplateView):
    template_name = 'core/team.html'

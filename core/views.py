from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from core.forms import LoginForm


class TeamView(TemplateView):
    template_name = 'core/team.html'


class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = "/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.login()
        return super().form_valid(form)
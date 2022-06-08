from django.shortcuts import render
from biblioteca_barcelona.templates import *
from biblioteca_barcelona.models import *
from django.views import View

# Create your views here.
class Home(View):
    template_name = "login.html"
    # allowed_methods = ["GET"]
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        print(request)

from .forms import FileServerUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpView(CreateView):
    form_class = FileServerUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
from django.views.generic import ListView, DetailView
from .models import File
import os
from django.http import FileResponse, Http404, HttpResponse
from django.views import View
from django.conf import settings
from django.db.models import Q
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import EmailForm



class FileDownloadView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to download files", status=403)
        
        file = File.objects.get(pk=pk)
        file_path = file.file.path
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file.title)
            return response
        raise Http404("File does not exist")
    

class FileListView(ListView):
    model = File
    template_name = 'files/files.html'
    context_object_name = 'files'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return File.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return super().get_queryset()


class FileDetailView(DetailView):
    model = File
    template_name = 'files/file_details.html'
    context_object_name = 'file'

    
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_instance = self.get_object()
        # Pass the current file instance to the form
        context['email_form'] = EmailForm(file_instance=file_instance)
        return context

def send_file_email(request, pk):
    file = File.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            # Sending the email with the file
            email = EmailMessage(
                'File from Our Platform',
                'Please find the attached file.',
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['email']]
            )
            email.attach_file(file.file.path)
            email.send()
            return redirect('files:details', pk=pk)
    else:
        form = EmailForm()

    return render(request, 'files/file_details.html', {'file': file, 'email_form': form})
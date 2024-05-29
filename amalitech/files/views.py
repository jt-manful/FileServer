from django.views.generic import ListView, DetailView
from .models import File, Download, EmailSent
from django.contrib.auth.decorators import login_required
import os
from django.db.models import Count
from django.http import FileResponse, Http404, HttpResponse
from django.views import View
from django.conf import settings
from django.db.models import Q
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import EmailForm, FileUploadForm
from datetime import datetime

class FileDownloaderView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # print("past here 1 req made")
        if not request.user.is_authenticated:
            # print("past here 2 not auth")
            return HttpResponse("You must be logged in to download files", status=403)
        # print("past here 3")

        file_instance = File.objects.get(pk=pk)
        # print("file instance title", file_instance.title)
        file_path = file_instance.file.path

        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_instance.title)
            Download.objects.create(file=file_instance, user=request.user, download_date=datetime.now())
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

    def get_queryset(self):
        return File.objects.all().annotate(
            total_downloads=Count('download'),
            total_emails=Count('emailsent')
        )

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return super().get_object(queryset=queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_instance = self.get_object()
        # print("file instance", file_instance.title)  # This should now work
        context['download_count'] = file_instance.total_downloads
        context['email_count'] = file_instance.total_emails
        context['email_form'] = EmailForm(file_instance=file_instance)  # Pass file_instance here
        return context

def send_file_email(request, pk):
    file = get_object_or_404(File, pk=pk)
    if request.method == 'POST':
        form = EmailForm(request.POST, file_instance=file)
        if form.is_valid():
            # Sending the email with the file
            email = EmailMessage(
                'File from Our Platform',
                'Please find the attached file.',
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['email']]
            )
            EmailSent.objects.create(file=file, user=request.user)

            email.attach_file(file.file.path)
            email.send()
            return redirect('files:file_details', pk=pk)
    else:
        form = EmailForm(file_instance=file)

    return render(request, 'files/file_details.html', {'file': file, 'email_form': form})

# 1. Should be able to upload files with a title and description 
class UploadFileView(View):
    def get(self, request):
        if not request.user.is_admin:
            return HttpResponse("You must be an admin to upload files", status=403)
        form = FileUploadForm()
        return render(request, 'files/upload_file.html', {'upload_form': form})

    def post(self, request):
        if not request.user.is_admin:
            return HttpResponse("You must be an admin to upload files", status=403)
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.uploaded_by = request.user
            new_file.save()
            return redirect('files:files')
        return render(request, 'files/upload_file.html', {'upload_form': form}) 
    

# 2. Should be able to see the number of downloads and number of emails sent for each file

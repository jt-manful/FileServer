from django.contrib import admin
from .models import File, Download

class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'upload_date', 'file')
    search_fields = ('title', 'description')
    list_filter = ('upload_date', 'uploaded_by')

  

class DownloadAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'download_date')
    search_fields = ('file__title', 'user__username')
    list_filter = ('download_date', 'user')


admin.site.register(File, FileAdmin)
admin.site.register(Download, DownloadAdmin)

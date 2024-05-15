from django.urls import path
from .views import FileListView, FileDetailView, FileDownloadView,send_file_email

app_name = 'files'

urlpatterns = [
    path('', FileListView.as_view(), name='files'),
    path('<int:pk>/', FileDetailView.as_view(), name='file_details'),
    path('download/<int:pk>/', FileDownloadView.as_view(), name='download'),
    path('send-email/<int:pk>/', send_file_email, name='send_email'),

]

# editor/urls.py

from django.urls import path
from .views import upload_file, finalize_pdf

urlpatterns = [
    path('', upload_file, name='upload_file'),
    path('finalize_pdf/', finalize_pdf, name='finalize_pdf'),  # Ensure this matches
]

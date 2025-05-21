# editor/forms.py

from django import forms

class FileUploadForm(forms.Form):
    pdf_file = forms.FileField(label='Upload PDF')
    overlay_image = forms.ImageField(label='Upload Overlay Image')

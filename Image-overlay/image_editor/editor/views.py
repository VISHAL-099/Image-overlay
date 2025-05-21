import os
import io
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import FileUploadForm
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            overlay_image = request.FILES['overlay_image']

            # Temporary save files and display them in the editor view
            pdf_path = handle_uploaded_file(pdf_file, 'pdf_files')
            overlay_path = handle_uploaded_file(overlay_image, 'overlay_images')
            return render(request, 'editor.html', {
                'pdf_path': pdf_path,
                'overlay_path': overlay_path
            })
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(file, folder_name):
    # Custom function to save uploaded files in media/uploads folder
    upload_dir = os.path.join('media', 'uploads', folder_name)
    os.makedirs(upload_dir, exist_ok=True)
    upload_path = os.path.join(upload_dir, file.name)

    with open(upload_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return f"/media/uploads/{folder_name}/{file.name}"

def finalize_pdf(request):
    if request.method == 'POST':
        # Retrieve file paths and overlay parameters from the POST request
        pdf_path = request.POST.get('pdf_path')
        overlay_path = request.POST.get('overlay_path')
        x = int(request.POST.get('x'))  # X position for overlay
        y = int(request.POST.get('y'))  # Y position for overlay
        scale = float(request.POST.get('scale', 1.0))  # Scale factor for overlay

        # Open PDF and overlay
        pdf_reader = PdfReader(pdf_path)
        pdf_writer = PdfWriter()
        overlay_image = Image.open(overlay_path)

        # Resize overlay image based on scale factor
        overlay_image = overlay_image.resize(
            (int(scale * overlay_image.width), int(scale * overlay_image.height)),
            Image.ANTIALIAS
        )

        for page in pdf_reader.pages:
            # Convert PDF page to image
            pdf_page = page.to_image()
            pdf_page.paste(overlay_image, (x, y), overlay_image)  # Paste overlay image

            # Add the modified page to the writer
            pdf_writer.add_page(pdf_page)

        # Send merged PDF back as response
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)

        response = HttpResponse(output, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="merged_document.pdf"'
        return response

    return HttpResponse(status=405)  # Method not allowed

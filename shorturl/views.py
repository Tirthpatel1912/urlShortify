from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import ShortURL
from django.shortcuts import render
from .forms import URLShortenerForm
from django.utils import timezone
from django.core.files import File
import qrcode
from io import BytesIO
from django.conf import settings
import os

import qrcode
from io import BytesIO
from django.core.files import File
from django.utils import timezone
import os
from django.conf import settings

def shorten_url(request):
    form = URLShortenerForm()
    short_url = None
    qr_code = None
    base_url = 'https://urlShortify'  # The base URL for shortened links

    if request.method == 'POST':
        form = URLShortenerForm(request.POST)
        if form.is_valid():
            # Save the ShortURL instance with the user-provided slug
            short_url_instance = form.save(commit=False)
            short_url_instance.created_at = timezone.now()  # Set the creation timestamp
            short_url_instance.save()  # Save the ShortURL instance to the database

            # Generate the shortened URL
            short_url = f"{base_url}/{short_url_instance.slug}/"

            # Generate a QR code if the URL is not private
            if not short_url_instance.is_private:
                # Generate the QR code image
                qr_img = qrcode.make(short_url)

                # Save the QR code to an in-memory file (BytesIO)
                qr_io = BytesIO()
                qr_img.save(qr_io, format='PNG')
                qr_io.seek(0)  # Reset the pointer of the file to the beginning

                # Define a filename and save the QR code to the model
                qr_code_filename = f"qr_codes/{short_url_instance.slug}_qr.png"
                short_url_instance.qr_code.save(qr_code_filename, File(qr_io))
                short_url_instance.save()  # Save again to store the QR code

            # Render the template with the short URL and QR code (if available)
            return render(request, 'shorturl_search_and_create.html', {
                'form': form,
                'short_url': short_url if short_url else None,
                'qr_code': short_url_instance.qr_code.url if short_url_instance.qr_code else None
            })

    return render(request, 'shorturl_search_and_create.html', {'form': form})



def search_url(request):
    # Check if the 'short_url' parameter is present in the query string
    short_url = request.GET.get('short_url')

    if short_url:
        # Extract the slug from the query parameter
        slug = short_url.split('/')[-1]
        try:
            # Look up the short URL object in the database
            url_obj = ShortURL.objects.get(slug=slug)

            # Check if the URL has expired
            if url_obj.expiration_date and timezone.now().date() > url_obj.expiration_date:
                return render(request, 'shorturl_search_and_create.html', {
                    'error': 'This URL has expired.'
                })

            # Increment the click count and log the click
            url_obj.increment_click_count()  # Call the method to update clicks and logs

            # Check if the URL is private and ask for a password
            if url_obj.is_private:
                if request.method == 'POST':
                    password = request.POST.get('password')
                    if password == url_obj.password:
                        return redirect(url_obj.long_url)  # Redirect to the original URL
                    else:
                        return render(request, 'shorturl_search_and_create.html', {
                            'error': 'Incorrect password.'
                        })
                return render(request, 'private_url_password.html', {'slug': slug})

            # If it's not private, redirect to the original URL
            return redirect(url_obj.long_url)

        except ShortURL.DoesNotExist:
            # If the short URL does not exist, show an error
            return render(request, 'shorturl_search_and_create.html', {
                'error': 'Shortened URL not found.'
            })

    # If no short_url parameter is provided, render the form to create a new one
    return render(request, 'shorturl_search_and_create.html')

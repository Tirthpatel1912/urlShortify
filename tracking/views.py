from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from shorturl.models import ShortURL  # Ensure this model has the necessary fields for tracking\
from django.http import HttpResponse
from io import BytesIO
import matplotlib.pyplot as plt
from collections import Counter
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from datetime import timedelta
import base64



@login_required
def track_url(request):
    short_url = request.GET.get('short_url')
    tracking_data = None
    graph = None

    if short_url:
        url_obj = get_object_or_404(ShortURL, slug=short_url)
        tracking_data = {
            'clicks': url_obj.click_count,
            'created_at': url_obj.created_at,
            'updated_at': url_obj.updated_at,
        }

        click_logs = url_obj.click_logs.all()
        click_times = [log.clicked_at for log in click_logs]  # Get the full datetime objects

        if click_times:
            # Count clicks per 10 minutes
            ten_minute_counts = Counter()
            for time in click_times:
                # Round down to the nearest 10 minutes
                ten_minute_key = time - timedelta(minutes=time.minute % 10, seconds=time.second, microseconds=time.microsecond)
                ten_minute_counts[ten_minute_key] += 1

            # Sort by ten-minute key
            minutes, counts = zip(*sorted(ten_minute_counts.items()))

            plt.figure(figsize=(12, 6))  # Increase figure size
            plt.plot(minutes, counts, marker='o', color='blue', linestyle='-', linewidth=2, markersize=5)  # Line graph

            plt.title('URL Clicks Over Time (Every 10 Minutes)')
            plt.xlabel('Time (10-Minute Intervals)')
            plt.ylabel('Number of Clicks')
            plt.xticks(rotation=45)

            # Format x-axis for better readability
            plt.xticks(minutes, [time.strftime('%H:%M') for time in minutes], rotation=45)

            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            plt.close()
            buffer.seek(0)
            graph = base64.b64encode(buffer.getvalue()).decode('utf-8')  # Encode to base64

    return render(request, 'track_url.html', {
        'short_url': short_url,
        'tracking_data': tracking_data,
        'graph': graph,
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('shorten_url')  # Redirect to the shorten URL page after signup
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

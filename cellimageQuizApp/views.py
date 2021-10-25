# from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Answer, Image, Profile
from django.shortcuts import redirect, render
#from django.template import loader
#from django.http import HttpResponse

# def index(request):
#    template = loader.get_template('index.html')
#    return HttpResponse(template.render(request=request))

##### create compte ######

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})


##### CONNECTED/DECONNECTED #####

def index(request):
    if request.user.is_authenticated:
        return render(request, "connected.html",
                      {"profile_user": Profile.objects.get(user_id=request.user.id),
                       "images": Image.objects.all().order_by('?')[0:24]})
    else:
        return render(request, "unconnected.html",
                      {"images": Image.objects.all().order_by('?')[0:24]})

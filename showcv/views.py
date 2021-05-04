from django.shortcuts import render, redirect
from butter_cms import ButterCMS
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ContactForm
from django.conf import settings

client = ButterCMS('a9c6436fe45c3afafed88780f488c53142d9f269')


def home(request):
    result = client.pages.get('*', 'mycv')
    data = result['data']['fields']
    dati = data['dati_personali']
    formazione = data['formazione']
    lingue = data['lingue']

    if request.method == 'GET':
       form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message + "\nfrom " + from_email, settings.EMAIL_HOST_USER, ['lucapedranzini01@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, "showcv/home.html", {'form': form, 'dati': dati, 'formazione': formazione, 'lingue': lingue})
    return render(request, "showcv/home.html", {'form': form, 'dati': dati, 'formazione': formazione, 'lingue': lingue})


def update(request):
    result = client.pages.get('*', 'mycv')
    data = result['data']['fields']
    dati = data['dati_personali']
    formazione = data['formazione']
    lingue = data['lingue']
    return render(request, "showcv/update.html", {'dati': dati, 'formazione': formazione, 'lingue': lingue})


# registration form
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        # initialise blank form and ip info
        form = RegisterForm()
    # render the page
    return render(request, "showcv/register.html", {"form": form, })


# handle logout
def logoutReq(request):
    logout(request)
    return redirect("/")


# handle login
def loginReq(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect('/')
            else:
                return render(request, "showcv/login.html", {"form": form})
        else:
            return render(request, "showcv/login.html", {"form": form})

    form = AuthenticationForm()
    return render(request, "showcv/login.html", {"form": form})

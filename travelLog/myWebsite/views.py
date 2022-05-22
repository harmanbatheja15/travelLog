from django.forms import modelformset_factory
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageForm, LogForm, RegistrationForm, AccountAuthenticationForm
from .models import *

def home(request):

    if(request.method == "POST"):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, phone=phone, message=message, date=datetime.today())
        contact.save()
        messages.success(request, f'Thanks {name}! We will get back to you soon.')

        return redirect('home')

    return render(request, "home.html")

def travelLogs(request):
    publicLogs = Log.objects.filter(visibility="public")
    context = {'publicLogs': publicLogs}
    return render(request, "travelLogs.html", context)

@login_required(login_url='signin')
def dashboard(request):
    if request.user.is_authenticated:
        log_user = request.user
        logs = Log.objects.filter(user=log_user)
        context = {
            'logs': logs,
        }

    return render(request, "dashboard.html", context)
    
def signup(request):

    context = {}

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            '''raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)'''

            messages.success(request, "Your account has been created successfully!")
            return redirect('signin')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, "signup.html", context)

def signin(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("/")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            messages.success(request, "You are logged in successfully!")

            if user:
                login(request, user)
                return redirect("/dashboard")

    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    
    return render(request, "signin.html", context)

def signout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='signin')
def addLog(request):

    if request.method == "POST":
        logForm = LogForm(request.POST, request.FILES)

        if logForm.is_valid():
            log = logForm.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, 'Log added successfully!')
            return redirect('/dashboard')

    else:
        logForm = LogForm()
    
    return render(request, "addLog.html", {'logForm': logForm})

@login_required(login_url='signin')
def editLog(request, log_id):
    logs = Log.objects.get(id=log_id)
    logForm = LogForm(request.POST or None, request.FILES or None, instance=logs)

    if logForm.is_valid():
        log = logForm.save(commit=False)
        log.user = request.user
        log.save()
        messages.success(request, 'Log Updated successfully!')
        return redirect('/dashboard')

    context = {
        'logForm': logForm,
        'logs': logs,
    }
    return render(request, "editLog.html", context)

def uploadImages(request, log_id):

    ImageFormSet = modelformset_factory(LogImage, form=ImageForm, extra=3)

    if request.method == "POST":
        logs = Log.objects.get(id=log_id)
        formset = ImageFormSet(request.POST, request.FILES, queryset=LogImage.objects.none())

        if formset.is_valid():
            for form in formset.cleaned_data:
                #this helps to not crash if the user do not upload all the photos
                if form:
                    image = form['image']
                    photo = LogImage(log=logs, image=image)
                    photo.save()
            messages.success(request, 'Images uploaded successfully!')
            return redirect('/dashboard')

    else:
        formset = ImageFormSet(queryset=LogImage.objects.none())

    return render(request, 'uploadImages.html', {'formset': formset})

def detail(request, log_id):
    log = get_object_or_404(Log, id=log_id)
    images = LogImage.objects.filter(log=log)
    ctx = {
        'logs': log,
        'images': images
    }

    obj = get_object_or_404(Log, id=log_id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, 'Log deleted successfully!')
        return redirect("/dashboard")

    return render(request, 'detail.html', ctx)

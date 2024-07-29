from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import UserRegisterForm

# Create your views here.
User = settings.AUTH_USER_MODEL

def RegisterView(request):
  if request.user.is_authenticated:
    return redirect("index")
    
  if request.method == "POST":
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
      new_user = form.save()
      username = form.cleaned_data.get("username")
      messages.success(request, f"Hey {username}, Account created.")

      # Authenticate user
      new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
      if new_user is not None:
        login(request, new_user)
        return redirect("index")
      else:
        messages.error(request, "Authentication failed.")
    else:
      messages.error(request, f"Form is not valid: {form.errors}")
  else:
    form = UserRegisterForm()

  context = {
    "form": form,
  }
  return render(request, "userauths/sign-up.html", context)

def loginView(request):
  if request.user.is_authenticated:
    return redirect("index")
    
  if request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
      user = User.objects.get(email=email)
    except:
      messages.error(request, "User does not exist")
        
    user = authenticate(request, email=email, password=password)

    if user is not None:
      login(request, user)
      messages.success(request, "You are logged in")
      return redirect("index")
    else:
      messages.error(request, "Username or Password, does not exist")
            
  return render(request, "userauths/sign-in.html")

def logoutView(request):
  logout(request)
  return redirect("sign-in")
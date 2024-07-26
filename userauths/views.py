from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login 
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
            
            # Debugging: Kiểm tra thông tin người dùng vừa tạo
            print(f"New user created: {new_user}")

            # Authenticate user
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            if new_user is not None:
                login(request, new_user)
                return redirect("index")
            else:
                messages.error(request, "Authentication failed.")
                # Debugging: Thông báo nếu xác thực không thành công
                print("Authentication failed")
        else:
            messages.error(request, f"Form is not valid: {form.errors}")
            # Debugging: Hiển thị lỗi form
            print(f"Form errors: {form.errors}")
    else:
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "userauths/sign-up.html", context)
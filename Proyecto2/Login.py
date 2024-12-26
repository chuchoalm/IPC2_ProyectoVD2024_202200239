from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Views for login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:  # Check if the user is an admin
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

# Admin dashboard
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponse('Acceso denegado', status=403)
    return render(request, 'admin_dashboard.html')

# User dashboard
@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return HttpResponse('Acceso denegado', status=403)
    return render(request, 'user_dashboard.html')

# URLs
from django.urls import path

urlpatterns = [
    path('', login_view, name='login'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
]

# Templates (login.html)
# Assuming templates are located in a directory named 'templates'.
# login.html:
"""
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Inicio de Sesión</h2>
    {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
    <form method="post">
        {% csrf_token %}
        <label for="username">Usuario:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Contraseña:</label><br>
        <input type="password" id="password" name="password"><br><br>
        <button type="submit">Ingresar</button>
    </form>
</body>
</html>
"""

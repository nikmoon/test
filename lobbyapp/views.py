from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    #user = authenticate(username='vasyan', password='director123')
    #print(type(user))
    users = [user.username for user in User.objects.all()]
    return HttpResponse('Hi человеки. ' + str(users))


def registration(request):
    return HttpResponse('Здесь у нас будет страничка регистрации. Загляните позже...')


def login(request):
    return HttpResponse('Здесь у нас будет страничка входа. Загляните позже...')


def logout(request):
    return HttpResponse('Сюда отправляются пользователи после выхода. Загляните позже...')


from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "../login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "lobbyapp/registration.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)



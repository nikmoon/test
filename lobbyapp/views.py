from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from lobby import settings
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
@login_required
def index(request):
    return HttpResponse('Hi человеки. ' + str(request.user))


def registration(request):
    return HttpResponse('Здесь у нас будет страничка регистрации. Загляните позже...')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'lobbyapp/login.html', RequestContext(request, {
            'form': AuthenticationForm(request),
            'next': request.GET['next'],
        }))
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'lobbyapp/login.html', RequestContext(request, {
                'form': AuthenticationForm(request),
                'next': request.POST['next'] or '/',
            }))
        else:
            login(request, user)
            return HttpResponseRedirect(request.POST['next'])
    else:
        return HttpResponseBadRequest('request method {} not allowed'.format(request.method))



def logout_view(request):
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



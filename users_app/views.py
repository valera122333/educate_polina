from django.shortcuts import render, redirect
from educate_portal.models import Standard
from users_app.forms import UserForm, UserProfileInfoForm, ProfileForm, ProfileForm2
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib import messages
from .models import UserProfileInfo


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("user_login")
        else:
            return HttpResponse("Пожалуйста используйте корректный логин и пароль")
            # return HttpResponseRedirect(reverse('register'))

    else:
        return render(request, 'users_app/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save(request.FILES)

            registered = True

            user = user_form.cleaned_data.get('username')
            messages.success(request, 'Аккаунт с именем ' +
                             user + ' успешно создан')
            return redirect('user_login')

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'users_app/registration.html',
                  {'registered': registered,
                   'user_form': user_form,
                   'profile_form': profile_form})


class HomeView(TemplateView):
    template_name = 'users_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standards = Standard.objects.all()
        teachers = UserProfileInfo.objects.filter(user_type='teacher')
        context['standards'] = standards
        context['teachers'] = teachers
        return context


def profile_editor(request):
    profile = UserProfileInfo.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = ProfileForm2(request.POST, instance=request.user)
        
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()

            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('profile_editor')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        form = ProfileForm(instance=profile)
        user_form = ProfileForm2(instance=request.user)

    context = {
        'user_form': user_form,
        'form': form,
        'user': request.user,
        'profile': profile,
    }

    return render(request, 'users_app/profile_editor.html', context)




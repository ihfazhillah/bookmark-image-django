from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Profile, Contact
from .forms import LoginForm, UserRegistrationForm, \
        UserEditForm, ProfileEditForm
from common.decorators import ajax_required
from actions.models import Action

# Create your views here.

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(pk=user_id)

            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
                Action.objects.create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})

    return JsonResponse({'status': 'ko'})



@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'accounts/user/list.html',
                  {'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request,
                  'accounts/user/detail.html',
                  {'user': user})

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Action.objects.create_action(user, 'has created an account')
            profile = Profile.objects.create(user=user)

            context = {
                'form': form
            }

            return render(request,
                          'accounts/register_done.html',
                          context)

    form = UserRegistrationForm()
    context = {
        'form': form
    }

    return render(request,
                  'accounts/register.html',
                  context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')

                return HttpResponse('disabled account')

        return HttpResponse('Invalid login')

    form = LoginForm()

    context = {
        'form': form
    }

    return render(request,
                  'accounts/login.html',
                  context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile updated successfully')
        else:
            messages.error(request, 'Ooops, there are some error with your profile')

    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        user_form = UserEditForm(instance=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request,
                  'accounts/edit_profile.html',
                  context)



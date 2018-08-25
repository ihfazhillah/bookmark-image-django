from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from actions.models import Action


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')


    context = {'actions': actions[:10]}

    return render(request,
                  'dashboard.html',
                  context)

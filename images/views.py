from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from .forms import ImageCreateForm
from .models import Image

from common.decorators import ajax_required
from actions.models import Action

import redis


r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

# Create your views here.

@login_required
def image_list(request):
    images = Image.objects.order_by('-id').all()
    paginator = Paginator(images, 4)
    page = request.GET.get('page', 1)

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'images': images})
    return render(request,
                  'images/image/list.html',
                  {'images': images})

@ajax_required
@login_required
@require_POST
def image_like(request):
    action = request.POST.get('action')
    image_id = request.POST.get('image_id')

    if action and image_id:
        try:
            image = Image.objects.get(pk=image_id)

            if action == 'like':
                image.users_like.add(request.user)
                Action.objects.create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
        except:
            pass
    return JsonResponse({'status': 'ok'})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, pk=id, slug=slug)
    total_views = r.incr('images:{}:views'.format(image.id))

    r.zincrby('images:rangking', image.id, 1)

    context = {
        'image': image,
        'total_views': total_views
    }
    
    return render(request,
                  'images/image/detail.html',
                  context)

@login_required
def image_rangking(request):
    img_rangking = r.zrange('images:rangking', 0, -1, desc=True)[:10]
    image_rangking_ids = [int(id) for id in img_rangking]
    most_viewed = list(Image.objects.filter(id__in=image_rangking_ids))
    most_viewed.sort(key=lambda x: image_rangking_ids.index(x.id))

    return render(request,
                  'images/image/rangking.html',
                  {'images': most_viewed})

@login_required
def create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)

        if form.is_valid():
            image_instance = form.save(commit=False)

            image_instance.user = request.user
            image_instance.save()

            Action.objects.create_action(request.user, 'bookmarked image', image_instance)

            messages.success(request, 'Image added successfully')
            return redirect(image_instance.get_absolute_url())
    else:
        form = ImageCreateForm(request.GET)

    context = {
        'form': form
    }

    return render(request,
                  'images/image/create.html',
                  context)



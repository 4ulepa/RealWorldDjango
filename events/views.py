from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Event, Category, Feature, Review


# Create your views here.
def event_list(request):
    context = {
        'events': Event.objects.all(),
        'categories': Category.objects.all(),
        'features': Feature.objects.all(),
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    percent = int((event.display_enroll_count() / event.participants_number)
                  * 100) if event.participants_number != 0 else 0
    context = {
        'event': event,
        'percent': percent
    }
    return render(request, 'events/event_detail.html', context)


@require_POST
def create_review(request):
    rate = request.POST.get('rate')
    text = request.POST.get('text')
    event_id = request.POST.get('event_id')
    response = {
        'ok': False,  # True если отзыв создан успешно, False в противном случае,
        'msg': '',  # Сообщение об ошибке
        'rate': rate,  # Оценка отзыва
        'text': text,  # Текст отзыва
        'created': '',  # Дата создания отзыва в формате DD.MM.YYYY
        'user_name': '',  # Полное имя пользователя
    }
    if request.user and request.user.is_authenticated:
        user = request.user
        response['user_name'] = str(user)
        if rate and text:
            if not Review.objects.filter(event=event_id, user=user).exists():
                try:
                    new_review = Review()
                    new_review.user = user
                    new_review.event = Event.objects.get(pk=event_id)
                    new_review.rate = rate
                    new_review.text = text
                    new_review.save()

                    response['created'] = str(new_review.created.strftime('%d.%m.%Y'))
                    response['ok'] = True
                except:
                    response['msg'] = 'Ошибка при создании отзыва'
            else:
                response['msg'] = 'Вы уже оставляли отзыв к этому событию'
        else:
            response['msg'] = 'Оценка и текст отзыва - обязательные поля'
    else:
        response['msg'] = 'Отзывы могут оставлять только зарегистрированные пользователи'
    return JsonResponse(response)

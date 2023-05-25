from socialweb.models import PostModel


def activities(request):
    if request.user.is_authenticated:
        cnt=PostModel.objects.filter(user=request.user).count()
        return {"pcnt":cnt}
    else:
        return {"pcnt":0}
    
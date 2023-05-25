from django.shortcuts import render,redirect
from socialweb.forms import RegistrationForm,LoginForm,ProfileAddForm,PostAddForm
from django.views.generic import View,CreateView,FormView,TemplateView,DeleteView,UpdateView,ListView,DetailView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from socialweb.models import UserProfileModel,PostModel,CommentModel
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
decs=[signin_required,never_cache]

class SignUpView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")

class SignInView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":self.form_class})
            

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    model=PostModel
    form_class=PostAddForm
    template_name="home.html"
    success_url=reverse_lazy("home")
    context_object_name="post"

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_queryset(self):
        return PostModel.objects.all().order_by("-created_date")
    

@method_decorator(decs,name="dispatch")
class ProfileView(CreateView):
    model=UserProfileModel
    form_class=ProfileAddForm
    template_name="profile-add.html"
    success_url=reverse_lazy("home")

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)


@method_decorator(decs,name="dispatch")
class ProfileDetailView(TemplateView):
    template_name="profile-detail.html"


@method_decorator(decs,name="dispatch")
class ProfileUpdateView(UpdateView):
    model=UserProfileModel
    form_class=ProfileAddForm
    template_name="profile-edit.html"
    success_url=reverse_lazy("home")
    pk_url_kwarg="id"

    
@method_decorator(decs,name="dispatch")
class AddCommentView(View):

    def post(self,request,*args,**kwargs):
        pid=kwargs.get("id")
        pos=PostModel.objects.get(id=pid)
        cmnt=request.POST.get("comment")
        usr=request.user
        CommentModel.objects.create(user=usr,post=pos,
        comment=cmnt)
        return redirect("home")
    

@method_decorator(decs,name="dispatch")
class LikePostView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        pos=PostModel.objects.get(id=id)
        pos.like.add(request.user)
        pos.save()
        return redirect("home")
    

@method_decorator(decs,name="dispatch")
class DislikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        pos=PostModel.objects.get(id=id)
        pos.like.remove(request.user)
        pos.save()
        return redirect("home")


@method_decorator(decs,name="dispatch")
class CommentLikePostView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        pos=CommentModel.objects.get(id=id)
        pos.clike.add(request.user)
        pos.save()
        return redirect("home")


@method_decorator(decs,name="dispatch")
class CommentDisikePostView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        pos=CommentModel.objects.get(id=id)
        pos.clike.remove(request.user)
        pos.save()
        return redirect("home")


@method_decorator(decs,name="dispatch")
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        PostModel.objects.get(id=id).delete()
        return redirect("home")


@method_decorator(decs,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")



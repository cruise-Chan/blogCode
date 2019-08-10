from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST， 表名用户正在访问注册页面，展示一个空的注册表单给用户
         form = RegisterForm

    return render(request, 'users/register.html', context={'form': form})


def index1(request):
    return render(request, 'users/index1.html')
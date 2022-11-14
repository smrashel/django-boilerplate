from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.db.models import Count, Q

from .models import *
from .forms import *
from .decorators import *

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect.')
    pagetitle = 'Login'
    context = {'pagetitle': pagetitle,}
    return render(request, 'authentication/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):  
    pagetitle = 'Dashboard'
    user_count = get_user_model().objects.all().count
    users = get_user_model().objects.all().values('groups__name').annotate(total=Count('id')).order_by('groups__name')

    context = {'pagetitle': pagetitle, 'user_count': user_count, 'users': users}
    return render(request, 'account/home.html', context)

def pagination(request, queryset, records_per_page):
    paginator = Paginator(queryset, records_per_page) # 1 records per page
    page = request.GET.get('page')
    if page is None:
        page=1
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(records_per_page)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    return queryset

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def users(request):
    pagetitle = 'Users'
    queryset = get_user_model().objects.all()
    user_group = request.user.groups.all()[0].name

    if request.method == 'POST':
        search_text = request.POST.get('search_text')
        employees = get_user_model().objects.filter(Q(employee_id=search_text) | Q(last_name__icontains=search_text) | Q(first_name__icontains=search_text) |
                                                         Q(email__icontains=search_text) | Q(username__icontains=search_text) | Q(contact_number__icontains=search_text))
        context = {'pagetitle': pagetitle, 'employees': employees, 'user_group': user_group}
        return render(request, 'account/user/users.html', context)
    
    # call the pagination function to paginate the queryset with records per page
    employees = pagination(request, queryset, 10)
    context = {'pagetitle': pagetitle, 'employees': employees, 'user_group': user_group}
    return render(request, 'account/user/users.html', context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def save_user_form(request, context, template_name):
    data = dict()
    if request.method == 'POST':
        form = context['form']
        if form.is_valid():
            fs = form.save(commit=False)
            fs.updated_by = request.user
            fs.updated_date = timezone.now()            
            fs.save()          
            fs.groups.clear()
            group = form.cleaned_data.get('groups')
            fs.groups.add(group[0].id)
            data['form_is_valid'] = True
            queryset = get_user_model().objects.all()
            user_group = request.user.groups.all()[0].name
            # call the pagination function to paginate the queryset with records per page
            employees = pagination(request, queryset, 10)
            data['html_user_list'] = render_to_string('account/user/user-table.html', {
                'employees': employees, 'user_group': user_group
            })
        else:
            data['form_is_valid'] = False
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def user_create(request):
    pagetitle = 'User Add'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        context = {'pagetitle': pagetitle, 'form': form,}
    else:
        form = CustomUserCreationForm()
        context = {'pagetitle': pagetitle, 'form': form,}
    return save_user_form(request, context, 'account/user/create.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def user_update(request, pk):
    pagetitle = 'User Update'
    user = get_object_or_404(get_user_model(), id=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        context = {'pagetitle': pagetitle, 'form': form,}
    else:
        form = CustomUserChangeForm(instance=user)
        context = {'pagetitle': pagetitle, 'form': form,}
    return save_user_form(request, context, 'account/user/update.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def user_delete(request, pk):
    pagetitle = 'User Delete'
    user = get_object_or_404(get_user_model(), id=pk)
    data = dict()
    if request.method == 'POST':
        user.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        queryset = get_user_model().objects.all()
        user_group = request.user.groups.all()[0].name
        # call the pagination function to paginate the queryset with records per page
        employees = pagination(request, queryset, 10)
        data['html_user_list'] = render_to_string('account/user/user-table.html', {
            'employees': employees, 'user_group': user_group
        })
    else:
        context = {'pagetitle': pagetitle, 'user': user}
        data['html_form'] = render_to_string('account/user/delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)


@login_required(login_url='login')
def change_password(request):
    heading = 'Change Password'
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
            context = {'form': form, 'heading': heading}
            return render(request, 'core/user/change_password.html', context)
    else:
        form = PasswordChangeForm(request.user)
        context = {'form': form, 'heading': heading}

    return render(request, 'account/user/change_password.html', context)
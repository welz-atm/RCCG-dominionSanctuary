from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import CommentForm, ServiceForm, PhotoForm, TitheForm, DonationForm
from .models import Comment, Service, Photo, Tithe, Donation
from django.core.paginator import Paginator
from authentication.decorators import worker_login_required, member_login_required, pastor_login_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from paystackapi.paystack import Paystack


def home(request):
    services = Service.objects.all().order_by('-date')[:6]
    if services.exists():
        context = {
            'services': services
        }
        return render(request, 'index.html', context)
    else:
        return render(request, '404.html', {})


def search_view(request):
    search_query = request.GET.get('search')
    if search_query is not None:
        qs = Service.objects.filter(name__contains=search_query).order_by('-date')
        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page')
        qs = paginator.get_page(page_number)
        context = {
             'qs': qs
          }
        return render(request, 'search.html', context)


@worker_login_required()
def create_service(request):
    if request.method == 'POST' and request.user.is_worker:
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.save()
            return redirect('all_services')
    else:
        form = ServiceForm(request.POST)
    context = {
        'form': form,
    }
    return render(request, 'add_service.html', context)


@worker_login_required()
def add_image_to_service(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return render(request, '404.html', {})
    if request.method == 'POST' and request.user.is_worker:
        photo_form = PhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.service = service
            photo.save()
            return redirect('all_services')
    else:
        photo_form = PhotoForm(request.POST)
    context = {
        'photo_form': photo_form,
    }
    return render(request, 'view_service.html', context)


@login_required()
def add_comment_to_service(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return render(request, '404.html', {})
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.save()
            service.comments.add(comment)
            return redirect('view_service')
    else:
        comment_form = CommentForm(request.POST)
    context = {
        'comment_form': comment_form,
    }
    return render(request, 'view_service.html', context)


def view_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    photos = Photo.objects.filter(service=service).select_related('service')
    context = {
        'service': service,
        'photos': photos
    }
    return render(request, 'view_service.html', context)


def all_services(request):
    services = Service.objects.all().order_by('-date')
    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    services = paginator.get_page(page_number)
    context = {
        'services': services
    }
    return render(request, 'all_services.html', context)


def view_gallery(request, pk):
    service = get_object_or_404(Service, pk=pk)
    photos = Photo.objects.filter(service=service).select_related('service')
    context = {
        'photos': photos,
        'service': service
    }
    return render(request, 'gallery.html', context)


@login_required()
def view_per_sunday(request):
    services = Service.objects.filter(name='Sunday Service').order_by('-date')
    if services.exists():
        paginator = Paginator(services, 10)
        page_number = request.GET.get('page')
        services = paginator.get_page(page_number)
        context = {
            'services': services
        }
        return render(request, 'search.html', context)
    else:
        return render(request, '404.html')


@login_required()
def view_per_sunday_special_service(request):
    services = Service.objects.filter(name='Sunday Special Service').order_by('-date')
    if services.exists():
        paginator = Paginator(services, 10)
        page_number = request.GET.get('page')
        services = paginator.get_page(page_number)
        context = {
            'services': services
        }
        return render(request, 'search.html', context)
    else:
        return render(request, '404.html')


@login_required()
def view_per_sunday_thanksgiving_service(request):
    services = Service.objects.filter(name='Sunday ThanksGiving Service').order_by('-date')
    if services.exists():
        paginator = Paginator(services, 10)
        page_number = request.GET.get('page')
        services = paginator.get_page(page_number)
        context = {
            'services': services
        }
        return render(request, 'search.html', context)
    else:
        return render(request, '404.html')


@login_required()
def view_per_tuesday(request):
    services = Service.objects.filter(name='Tuesday Bible Study').order_by('-date')
    if services.exists():
        paginator = Paginator(services, 10)
        page_number = request.GET.get('page')
        services = paginator.get_page(page_number)
        context = {
            'services': services
        }
        return render(request, 'search.html', context)
    else:
        return render(request, '404.html')


@login_required()
def view_per_thursday(request):
    services = Service.objects.filter(name='Thursday Revival Service').order_by('-date')
    if services.exists():
        paginator = Paginator(services, 10)
        page_number = request.GET.get('page')
        services = paginator.get_page(page_number)
        context = {
            'services': services
        }
        return render(request, 'search.html', context)
    else:
        return render(request, '404.html')


@login_required()
def edit_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return render(request, '404.html', {})
    if request.method == 'POST' and request.user.is_authenticated and request.user == comment.user:
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('view_message')
    else:
        comment_form = CommentForm(request.POST)
    context = {
        'comment_form': comment_form,
        'comment': comment
    }
    return render(request, 'view_message.html', context)


@login_required()
def pay_tithe(request):
    if request.method == 'POST':
        form = TitheForm(request.POST)
        if form.is_valid():
            tithe = form.save(commit=False)
            amount = tithe.amount * 100
            paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
            response = paystack.transaction.initialize(amount=amount, email=request.user.email,
                                                       callback_url='http://localhost:8000/confirm_tithe/')
            url = response['data']['authorization_url']
            reference = response['data']['reference']
            tithe.user = request.user
            tithe.reference = reference
            tithe.save()
            return redirect(url)
    else:
        form = TitheForm()
    context = {
        'form': form
    }
    return render(request, 'pay_tithe.html', context)
    
    
@login_required()
def test_pay_tithes(request):
    amount = request.POST["amount"]
    month = request.POST["month"]
    total = amount * 100
    paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
    response = paystack.transaction.initialize(amount=total, email=request.user.email,
                                           callback_url='http://localhost:8000/confirm_tithe/')
    url = response.data['authorization_url']
    reference = response.data['reference']
    tithe = Tithe(user=request.user)
    tithe.amount = total
    tithe.reference = reference
    tithe.month = month
    tithe.save()
    return redirect(url)


@login_required()
def confirm_tithe(request):
    tithes = Tithe.objects.filter(user=request.user).order_by('-date')
    tithe = tithes[0]
    paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
    response = paystack.transaction.verify(reference=tithe.reference)
    tithe.transaction_date = response['data']['transaction_date']
    tithe.status = response['data']['status']
    tithe.save()
    paginator = Paginator(tithes, 10)
    page_number = request.GET.get('page')
    tithes = paginator.get_page(page_number)
    context = {
        'tithes': tithes
    }
    return render(request, 'tithes.html', context)


def all_tithes(request):
    tithes = Tithe.objects.all().order_by('date')
    paginator = Paginator(tithes, 10)
    page_number = request.GET.get('page')
    tithes = paginator.get_page(page_number)
    context = {
        'tithes': tithes
    }
    return render(request, 'tithes.html', context)


def my_tithes(request):
    tithes = Tithe.objects.filter(user=request.user).order_by('date').select_related('user')
    paginator = Paginator(tithes, 10)
    page_number = request.GET.get('page')
    tithes = paginator.get_page(page_number)
    context = {
        'tithes': tithes
    }
    return render(request, 'tithes.html', context)


def create_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            amount = donation.amount * 100
            paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
            response = paystack.transaction.initialize(amount=amount, email=donation.email,
                                                       callback_url='http://localhost:8000/confirm_donation/')
            url = response['data']['authorization_url']
            reference = response['data']['reference']
            donation.reference = reference
            donation.save()
            return redirect(url)
    else:
        form = DonationForm()
    context = {
        'form': form
    }
    return render(request, 'make_donation.html', context)


def confirm_donation(request):
    return render(request, 'success.html', {})

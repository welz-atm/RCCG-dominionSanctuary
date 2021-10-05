from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm, ServiceForm, PhotoForm, TitheForm, DonationForm
from .models import Comment, Service, Photo, Tithe, Donation
from django.db.models import Sum
from django.http import JsonResponse
from django.core.paginator import Paginator
from authentication.decorators import worker_login_required, member_login_required, pastor_login_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from paystackapi.paystack import Paystack
import os
import cloudinary

cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
    secure=True
)


def home(request):
    services = Service.objects.all().order_by('-date')[:9]
    if services.exists():
        context = {
            'services': services
        }
        return render(request, 'index.html', context)
    else:
        return render(request, '404.html', {})


def search_view(request):
    search_query = request.GET.get('search_query')
    if search_query is not None:
        services = Service.objects.filter(name__contains=search_query)
        paginator = Paginator(services, 12)
        page_number = request.GET.get('page')
        services = paginator.get_page(page_number)
        context = {
            'services': services,
            'search_query': search_query

          }
        return render(request, 'search.html', context)


def create_service(request):
    if request.method == 'POST' and request.user.is_admin:
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            response = cloudinary.uploader.upload_large(request.FILES['video'], resource_type='video', quality='auto:eco')
            service.video = response['secure_url']
            service.save()
            return redirect('all_services')
    else:
        form = ServiceForm(request.POST)
    context = {
        'form': form,
    }
    return render(request, 'add_service.html', context)


def add_image_to_service(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return render(request, '404.html', {})
    if request.method == 'POST' and request.user.is_admin:
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


def view_praise_worship(request, pk):
    service = get_object_or_404(Service, pk=pk)
    context = {
        'service': service,
    }
    return render(request, 'view_praise_worship.html', context)


def all_services(request):
    services = Service.objects.all().order_by('-date')
    paginator = Paginator(services, 12)
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
    services = Service.objects.filter(name='Sunday Service').order_by('date')
    if services.exists():
        paginator = Paginator(services, 12)
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
    services = Service.objects.filter(name='Sunday Special Service').order_by('date')
    if services.exists():
        paginator = Paginator(services, 12)
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
    services = Service.objects.filter(name='Sunday ThanksGiving Service').order_by('date')
    if services.exists():
        paginator = Paginator(services, 12)
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
    services = Service.objects.filter(name='Tuesday Bible Study').order_by('date')
    if services.exists():
        paginator = Paginator(services, 12)
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
    services = Service.objects.filter(name='Thursday Revival Service').order_by('date')
    if services.exists():
        paginator = Paginator(services, 12)
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
                                                       callback_url='https://rccgdom.herokuapp.com/confirm_tithe/')
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
def confirm_tithe(request):
    tithe_url = request.build_absolute_uri()
    reference = tithe_url.split('=')[2]
    paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
    response = paystack.transaction.verify(reference=reference)
    tithes = Tithe.objects.filter(user=request.user).order_by('-date').select_related('user')
    tithe = tithes[0]
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


@login_required()
def all_tithes(request):
    if request.user.is_admin:
        tithes = Tithe.objects.all().order_by('date')
        paginator = Paginator(tithes, 12)
        page_number = request.GET.get('page')
        tithes = paginator.get_page(page_number)
        context = {
            'tithes': tithes
        }
        return render(request, 'tithes.html', context)
    else:
        return render(request, '404.html', {})

@login_required()
def my_tithes(request):
    tithes = Tithe.objects.filter(user=request.user).order_by('date').select_related('user')
    paginator = Paginator(tithes, 12)
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
                                                       callback_url='https://rccgdom.herokuapp.com/confirm_donation/')
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


@login_required()
def all_donations(request):
    if request.user.is_admin:
        donations = Donation.objects.all().order_by('date')
        paginator = Paginator(donations, 12)
        page_number = request.GET.get('page')
        donations = paginator.get_page(page_number)
        context = {
            'donations': donations
        }
        return render(request, 'donations.html', context)
    else:
        return render(request, '404.html', {})


def individual_tithe_chart(request):
    labels = []
    data = []
    tithes = Tithe.objects.values('user__email').annotate(tithe_total=Sum('amount'))
    for info in tithes:
        labels.append(info['user__email'])
        data.append(info['tithe_total'])
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def confirm_donation(request):
    donation_url = request.build_absolute_uri()
    reference = donation_url.split('=')[2]
    paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
    response = paystack.transaction.verify(reference=reference)
    donation = Donation.objects.get(reference=reference)
    donation.transaction_date = response['data']['transaction_date']
    donation.status = response['data']['status']
    donation.save()
    return render(request, 'success.html', {})

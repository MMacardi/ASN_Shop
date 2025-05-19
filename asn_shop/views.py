from django.shortcuts import render, get_object_or_404, redirect
from .forms import MyUserRegistrationForm, CarForm, CarImageForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import CarImage, Car
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def home_page(request):
    cars = Car.objects.all()  # Get all cars
    return render(request, 'asn_shop/home_page.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)  # Get car by ID
    car_images = car.images.all()  # Get all images for this car
    return render(request, 'asn_shop/car_detail.html', {'car': car, 'car_images': car_images})

@login_required
def add_car(request):
    if not request.user.is_seller:
        return HttpResponseForbidden("Only sellers can add cars.")

    if request.method == 'POST':
        car_form = CarForm(request.POST)
        images = request.FILES.getlist('images')

        if car_form.is_valid():
            car = car_form.save(commit=False)
            car.seller = request.user
            car.save()

            for image in images:
                CarImage.objects.create(car=car, image=image)

            return redirect('home')

    else:
        car_form = CarForm()

    return render(request, 'asn_shop/add_car.html', {'car_form': car_form})

@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, seller=request.user)
    car_images = car.images.all()

    if request.method == 'POST':
        car_form = CarForm(request.POST, instance=car)

        if car_form.is_valid():
            car_form.save()

            # Delete images
            delete_images_ids = request.POST.getlist('delete_images')
            if delete_images_ids:
                CarImage.objects.filter(id__in=delete_images_ids, car=car).delete()

            # Add new images
            images = request.FILES.getlist('images')
            for image in images:
                CarImage.objects.create(car=car, image=image)

            return redirect('car_detail', car_id=car.id)

    else:
        car_form = CarForm(instance=car)

    return render(request, 'asn_shop/edit_car.html', {
        'car_form': car_form,
        'car_images': car_images,
        'car': car
    })

@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    # Check if current user is seller and owner of the car
    if car.seller != request.user:
        return HttpResponseForbidden("You cannot delete this car.")
    
    if request.method == 'POST':
        car.delete()
        return redirect('home')
    
    return render(request, 'asn_shop/delete_car.html', {'car': car})

from django.contrib import messages
from django.contrib.auth import login, logout

def register(request):
    if request.method == 'POST':
        form = MyUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! You have successfully registered.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = MyUserRegistrationForm()
    return render(request, 'asn_shop/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('home')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')  # already logged in

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"You are logged in as {user.email}.")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'asn_shop/login.html', {'form': form})

from .forms import ReviewForm

def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    images = car.images.all()
    reviews = car.review_set.all()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            return redirect('car_detail', car_id=car.id)
    else:
        review_form = ReviewForm()

    return render(request, 'asn_shop/car_detail.html', {
        'car': car,
        'images': images,
        'reviews': reviews,
        'review_form': review_form,
    })

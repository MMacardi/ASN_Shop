from django.shortcuts import render, get_object_or_404, redirect
from .forms import MyUserRegistrationForm, CarForm, CarImageForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import CarImage, Car
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm



def home_page(request):
    cars = Car.objects.all()  # Получаем все автомобили
    return render(request, 'asn_shop/home_page.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)  # Получаем автомобиль по ID
    car_images = car.images.all()  # Получаем все изображения для этого автомобиля
    return render(request, 'asn_shop/car_detail.html', {'car': car, 'car_images': car_images})

@login_required
def add_car(request):
    if not request.user.is_seller:
        return HttpResponseForbidden("Только продавцы могут добавлять авто.")

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

            # ✅ Удаление изображений
            delete_images_ids = request.POST.getlist('delete_images')
            if delete_images_ids:
                CarImage.objects.filter(id__in=delete_images_ids, car=car).delete()

            # ✅ Добавление новых изображений
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
    
    # Проверка, является ли текущий пользователь продавцом и владельцем автомобиля
    if car.seller != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот автомобиль.")
    
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
            messages.success(request, f"Добро пожаловать, {user.username}! Вы успешно зарегистрировались.")
            return redirect('home')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = MyUserRegistrationForm()
    return render(request, 'asn_shop/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect('home')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')  # если уже залогинен

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Вы вошли как {user.email}")
            return redirect('home')
        else:
            messages.error(request, "Неверный email или пароль")
    else:
        form = AuthenticationForm()

    return render(request, 'asn_shop/login.html', {'form': form})
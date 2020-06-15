from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ImageForm


@login_required
def create_image(request):
    if request.method == 'POST':
        # Форма отправлена.
        form = ImageForm(data=request.POST)
        if form.is_valid():
            # Данные формы валидны.
            new_item = form.save(commit=False)
            # Добавляем пользователя к созданному объекту.
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения.
            return redirect(new_item.get_absolute_url())
    else:
        # Заполняем форму данными из GET-запроса.
        form = ImageForm(data=request.GET)
        return render(request, 'images/create.html', {'section': 'images', 'form': form})

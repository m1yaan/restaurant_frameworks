from django import forms
from django.utils import timezone
from .models import Order, Client, Dish
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "phone", "email"]
        widgets = {"name": forms.TextInput(attrs={"class":"form-control"}), "phone": forms.TextInput(attrs={"class":"form-control"}), "email": forms.EmailInput(attrs={"class":"form-control"})}
class OrderForm(forms.ModelForm):
    guests = forms.IntegerField(min_value=1, initial=1, label="Количество гостей", widget=forms.NumberInput(attrs={"class":"form-control"}))
    class Meta:
        model = Order
        fields = ["client", "table", "status", "reservation_at"]
        widgets = {"client": forms.Select(attrs={"class":"form-select"}), "table": forms.Select(attrs={"class":"form-select"}), "status": forms.Select(attrs={"class":"form-select"}), "reservation_at": forms.DateTimeInput(attrs={"class":"form-control", "type":"datetime-local"}, format="%Y-%m-%dT%H:%M")}
    def clean_reservation_at(self):
        value = self.cleaned_data["reservation_at"]
        if value < timezone.now():
            raise forms.ValidationError("Дата и время заказа не могут быть в прошлом.")
        return value
    def clean(self):
        cleaned = super().clean()
        table, guests = cleaned.get("table"), cleaned.get("guests")
        if table and not table.is_active:
            self.add_error("table", "Этот стол временно недоступен.")
        if table and guests and table.capacity < guests:
            self.add_error("table", f"Вместимость стола — {table.capacity}, гостей — {guests}.")
        return cleaned
class DishPhotoForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["photo"]

from django.db import models
from django.core.validators import MinValueValidator


class Client(models.Model):
    name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=20, unique=True)
    email = models.EmailField("Email", blank=True)
    def __str__(self): return self.name

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class Table(models.Model):
    number = models.PositiveIntegerField("Номер", unique=True)
    capacity = models.PositiveIntegerField("Вместимость", validators=[MinValueValidator(1)])
    is_active = models.BooleanField("Активен", default=True)
    def __str__(self): return f"Стол №{self.number}"

    class Meta:
        verbose_name = "стол"
        verbose_name_plural = "столы"


class Dish(models.Model):
    name = models.CharField("Название", max_length=120)
    category = models.CharField("Категория", max_length=80)
    price = models.DecimalField(
        "Цена",
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(0)])
    is_available = models.BooleanField("В меню", default=True)
    photo = models.ImageField("Фото", upload_to="dishes/", blank=True, null=True)
    def __str__(self): return self.name

    class Meta:
        verbose_name = "блюдо"
        verbose_name_plural = "блюда"


class Order(models.Model):
    STATUS_CHOICES = [("new", "Новый"), ("cooking", "Готовится"),
                      ("ready", "Готов"), ("paid", "Оплачен"), ("cancelled", "Отменён")]
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Клиент")
    table = models.ForeignKey(
        Table,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Стол")
    dishes = models.ManyToManyField(
        Dish,
        through="OrderItem",
        related_name="orders",
        verbose_name="Блюда")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    reservation_at = models.DateTimeField(
        "Дата и время бронирования", default=__import__(
            "django.utils.timezone", fromlist=["now"]).now)

    def __str__(self): return f"Заказ №{self.pk}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "заказ"
        verbose_name_plural = "заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    def __str__(self): return f"{self.dish} × {self.quantity}"

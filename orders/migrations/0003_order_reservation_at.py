import django.utils.timezone
from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [("orders", "0002_dish_photo")]
    operations = [
        migrations.AddField(
            model_name="order",
            name="reservation_at",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Дата и время бронирования"),
        ),
    ]

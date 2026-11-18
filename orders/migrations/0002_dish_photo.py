from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [("orders", "0001_initial")]
    operations = [migrations.AddField(model_name="dish", name="photo", field=models.ImageField(blank=True, null=True, upload_to="dishes/", verbose_name="Фото"))]

from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PlantScan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="scans/%Y/%m/%d/")),
                ("scan_type", models.CharField(choices=[("plant","Plant"),("crop","Crop"),("flower","Flower"),("lawn","Lawn / Grass"),("tree","Tree / Shrub")], max_length=20)),
                ("plant_name", models.CharField(blank=True, max_length=120)),
                ("scientific_name", models.CharField(blank=True, max_length=160)),
                ("likely_condition", models.CharField(blank=True, max_length=180)),
                ("confidence", models.CharField(blank=True, max_length=20)),
                ("severity", models.CharField(blank=True, max_length=20)),
                ("symptoms", models.JSONField(blank=True, default=list)),
                ("explanation", models.TextField(blank=True)),
                ("alternative_conditions", models.JSONField(blank=True, default=list)),
                ("treatment", models.JSONField(blank=True, default=list)),
                ("prevention", models.JSONField(blank=True, default=list)),
                ("sources", models.JSONField(blank=True, default=list)),
                ("model_version", models.CharField(blank=True, max_length=80)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]

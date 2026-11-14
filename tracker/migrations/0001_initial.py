import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("company", models.CharField(max_length=120)),
                ("position", models.CharField(max_length=120)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("wishlist", "Wishlist"),
                            ("applied", "Applied"),
                            ("interview", "Interview"),
                            ("offer", "Offer"),
                            ("rejected", "Rejected"),
                        ],
                        default="applied",
                        max_length=20,
                    ),
                ),
                ("applied_date", models.DateField(default=django.utils.timezone.localdate)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("job_url", models.URLField(blank=True)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-applied_date", "-created_at"],
            },
        ),
    ]

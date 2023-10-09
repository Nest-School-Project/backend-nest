# Generated by Django 4.2.6 on 2023-10-09 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_assessment'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.JSONField(default={})),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.assessment')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.grades')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.student')),
                ('theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.theme')),
            ],
        ),
    ]

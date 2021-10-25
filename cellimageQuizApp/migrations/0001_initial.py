# Generated by Django 3.0.3 on 2021-10-19 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField()),
                ('answer', models.CharField(max_length=255)),
                ('definition', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('microscopy', models.CharField(max_length=255)),
                ('cell_type', models.CharField(max_length=255)),
                ('component', models.CharField(max_length=255)),
                ('doi', models.CharField(max_length=255)),
                ('organism', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('imageField', models.CharField(max_length=255)),
                ('points', models.IntegerField()),
                ('n_answer', models.IntegerField()),
                ('n_image', models.IntegerField()),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cellimageQuizApp.Image')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.IntegerField(default=0)),
                ('component_score', models.IntegerField(default=0)),
                ('microscopy_score', models.IntegerField(default=0)),
                ('level', models.CharField(default='beginner', max_length=50)),
                ('user', models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
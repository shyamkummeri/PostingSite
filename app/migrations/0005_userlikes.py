# Generated by Django 2.2.10 on 2021-01-23 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLikes',
            fields=[
                ('likesid', models.AutoField(primary_key=True, serialize=False)),
                ('like', models.BooleanField()),
                ('postidlikes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.PostContent')),
                ('useridlikes', models.ManyToManyField(blank=True, to='app.UserRegister')),
            ],
        ),
    ]
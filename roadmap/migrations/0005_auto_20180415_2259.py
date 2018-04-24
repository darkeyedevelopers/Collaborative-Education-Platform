# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-15 17:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0004_resource_roadmap'),
    ]

    operations = [
        migrations.CreateModel(
            name='Downvote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='roadmap',
            old_name='downvotes',
            new_name='downcount',
        ),
        migrations.RenameField(
            model_name='roadmap',
            old_name='upvotes',
            new_name='upcount',
        ),
        migrations.AddField(
            model_name='upvote',
            name='roadmap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmap.Roadmap'),
        ),
        migrations.AddField(
            model_name='downvote',
            name='roadmap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmap.Roadmap'),
        ),
    ]
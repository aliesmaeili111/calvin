# Generated by Django 4.0 on 2023-05-20 08:08

import ckeditor.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='لطفا بیشتر از 250 حرف ننویسید', max_length=250, validators=[django.core.validators.MaxLengthValidator(250, 'لطفا بین 1 تا 250 حرف بنویسید')], verbose_name='عنوان مقاله')),
                ('slug', models.SlugField(help_text='لطفا بیشتر از 35 حرف ننویسید', max_length=35, unique=True, validators=[django.core.validators.MaxLengthValidator(35, 'لطفا بین 1 تا 35 حرف بنویسید')], verbose_name='آدرس مقاله')),
                ('description', ckeditor.fields.RichTextField(help_text='محتوایی برای مقاله خود بنویسید', verbose_name='محتوای مقاله')),
                ('thumbnail', models.ImageField(help_text='برای مقاله تصویری انتخاب کنید', upload_to='images', verbose_name='تصویر مقاله')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, help_text='فرمت صحیح تاریخ YYYY-MM-DD', verbose_name='زمان انتشار')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('d', 'پیش نویس'), ('p', 'منتشر شده'), ('i', 'در حال بررسی'), ('b', ' برگشت داده شده')], help_text='وضعیت مقاله را انتخاب کنید', max_length=1, verbose_name='وضعیت')),
                ('author', models.ForeignKey(help_text='یک نویسنده کارمندی را انتخاب کنید', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='account.user', verbose_name='نویسنده')),
            ],
            options={
                'verbose_name': 'مقاله',
                'verbose_name_plural': 'مقالات',
                'ordering': ['-publish'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='از 1 تا 200 حرف بنویسید', max_length=200, validators=[django.core.validators.MaxLengthValidator(200, 'لطفا بین 1 تا 200 حرف بنوسید')], verbose_name='عنوان دسته بندی')),
                ('slug', models.SlugField(help_text='از 1 تا 30 حرف بنویسید', max_length=30, unique=True, validators=[django.core.validators.MaxLengthValidator(30, 'لطفا بین 1 تا 30 حرف بنوسید')], verbose_name='آدرس دسته بندی')),
                ('status', models.BooleanField(default=True, help_text='آیا نمایش داده شود ؟', verbose_name='نمایش دادن')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('position', models.IntegerField(default=1000, unique=True, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(1000000000)], verbose_name='موقعیت')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='لطفا نام و نام خانوادگی خود را وارد کنید', max_length=35, verbose_name='نام و نام خانوادگی')),
                ('email', models.EmailField(help_text='ایمیل خود را وارد کنید', max_length=254, verbose_name='ایمیل')),
                ('context', models.TextField(help_text='متن مورد نظر خود را وارد کنید', verbose_name='محتوا')),
            ],
            options={
                'verbose_name': 'مخاطب',
                'verbose_name_plural': 'مخاطبان',
            },
        ),
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آدرس آی پی')),
            ],
            options={
                'verbose_name': 'آدرس آی پی',
                'verbose_name_plural': 'آدرس ها',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(help_text='نظر خود را بنویسید', max_length=10000, verbose_name='کامنت')),
                ('active', models.BooleanField(default=False, help_text='در سایت نمایش داده شود ؟', verbose_name='فعال')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, help_text='فرمت صحیح تاریخ YYYY-MM-DD', verbose_name='تاریخ انتشار')),
                ('article', models.ForeignKey(help_text='لطفا یک مقاله برای نظر دادن انتخاب کنید', on_delete=django.db.models.deletion.CASCADE, to='blog.article', verbose_name='مقاله')),
                ('user', models.ForeignKey(help_text='کاربر خود را انتخاب کنید', null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.user', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظر ها',
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(help_text='کنترل یا فرمان را در مک نگه دارید تا بیش از یک مورد انتخاب شود|', related_name='articles', to='blog.Category', verbose_name='دسته بندی'),
        ),
        migrations.AddField(
            model_name='article',
            name='hits',
            field=models.ManyToManyField(blank=True, related_name='hits', to='blog.IPAddress', verbose_name='آدرس آی پی'),
        ),
    ]

from django.utils import timezone
from django.db import models
import random
from django.urls import reverse
from django.contrib.auth.models import User
import os


class Standard(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name="Заголовок категории")
    slug = models.SlugField(null=True, blank=True,verbose_name="Название в адресной строке")
    description = models.TextField(max_length=500, blank=True,verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет обучения'
        verbose_name_plural = 'Предмет обучения'


def save_subject_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.subject_id:
        filename = 'Subject_Pictures/{}.{}'.format(instance.subject_id, ext)
    return os.path.join(upload_to, filename)


class Subject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True,verbose_name="айди подкатегории")
    name = models.CharField(max_length=100,verbose_name="название")
    slug = models.SlugField(null=True, blank=True,verbose_name="подкатегория в адресной строке")
    standard = models.ForeignKey(
        Standard, on_delete=models.CASCADE, related_name='subjects')
    image = models.ImageField(
        upload_to=save_subject_image, blank=True, verbose_name='Изображение подкатегории')
    description = models.TextField(max_length=500, blank=True,verbose_name="Описание подкатегории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория предмета обучения'
        verbose_name_plural = 'Категория предмета обучения'


def save_lesson_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.lesson_id:
        filename = 'lesson_files/{}/{}.{}'.format(
            ext)
        if os.path.exists(filename):
            new_name = str(instance.name) + str('1')
            filename = 'lesson_images/{}/{}.{}'.format(
                instance.name, new_name, ext)
    return os.path.join(upload_to, filename)


class Lesson(models.Model):

    Standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="автор урока")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="дата создания")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=250, verbose_name="Заголовок урока")
    description = models.TextField(
        max_length=5000, blank=True, verbose_name="Описание урока")
    description2 = models.TextField(
        max_length=5000, blank=True, verbose_name="Продолжение описания")
    position = models.PositiveSmallIntegerField(verbose_name="Номер урока")
    slug = models.SlugField(
        null=True, blank=True, verbose_name='уникальное поле в адресной строке (eng раскладка)')


    file = models.FileField(upload_to='videos/', null=True, blank=True,verbose_name="видео")

    ppt = models.FileField(upload_to=save_lesson_files,
                        blank=True,verbose_name="презентация(необязательное поле)")
    Notes = models.FileField(upload_to=save_lesson_files,
                             blank=True,verbose_name="урок в виде ворда/пдф(необязательное поле)")
    console = models.URLField(
        max_length=250, default='',verbose_name="возможность писать код, взяли с trinket io")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('educate_portal:lesson_list', kwargs={'slug': self.subject.slug, 'standard': self.Standard.slug})

    class Meta:
        verbose_name = 'Уроки'
        verbose_name_plural = 'Уроки'


class Comment(models.Model):
    lesson_name = models.ForeignKey(
        Lesson, null=True, on_delete=models.CASCADE, related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = (
            "комментарий от" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']

    class Meta:
        verbose_name = 'комментарии'
        verbose_name_plural = 'комментарии'


class Reply(models.Model):
    comment_name = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    reply_body = models.TextField(
        max_length=500, verbose_name='ответ на комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Ответ на комментарий " + str(self.comment_name.comm_name)

    class Meta:
        verbose_name = 'Ответы на комментарии'
        verbose_name_plural = 'Ответы на комментарии'
# Create your models here.

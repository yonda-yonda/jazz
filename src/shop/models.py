import uuid
from django.db import models

class Publisher(models.Model):
    class Meta:
        db_table = 'publisher'
        verbose_name = verbose_name_plural = '出版社'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='出版社名', max_length=255)
    created_at = models.DateTimeField(verbose_name='登録日時',
                                      auto_now_add=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    class Meta:
        db_table = 'author'
        verbose_name = verbose_name_plural = '著者'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='著者名', max_length=255)
    created_at = models.DateTimeField(verbose_name='登録日時',
                                      auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    class Meta:
        db_table = 'book'
        verbose_name = verbose_name_plural = '本'

    stars = ((1, '☆'), (2, '☆☆'), (3, '☆☆☆'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='タイトル', max_length=20)
    price = models.IntegerField(verbose_name='価格', null=True, blank=True)
    publisher = models.ForeignKey(Publisher, verbose_name='出版社', 
                                  on_delete=models.PROTECT)
    authors = models.ManyToManyField(Author, verbose_name='著者')
    star = models.PositiveSmallIntegerField(verbose_name='評価', 
                                            choices=stars, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='登録日時',
                                      auto_now_add=True)

    def __str__(self):
        return self.title
    

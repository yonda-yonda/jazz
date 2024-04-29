from django.contrib import admin

from .models import Book, Publisher, Author


class BookModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'id', 'publisher', '_authors', 'star', 'created_at')
    ordering = ('-created_at', )
    readonly_fields = ('id', 'created_at')

    def _authors(self, row):
        return ','.join([x.name for x in row.authors.all()])

class AuthorModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at')
    ordering = ('-created_at', )
    readonly_fields = ('id', 'created_at')

class PublisherModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at')
    ordering = ('-created_at', )
    readonly_fields = ('id', 'created_at')


admin.site.register(Book, BookModelAdmin)
admin.site.register(Author, AuthorModelAdmin)
admin.site.register(Publisher, PublisherModelAdmin)

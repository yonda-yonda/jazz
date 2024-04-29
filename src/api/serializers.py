from rest_framework import serializers

from shop.models import Book, Author, Publisher


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'authors', 'publisher', 'star']
        extra_kwargs = {
            'title': {
                'error_messages': {
                    'blank': 'タイトルは空にできません。',
                }
            },
            'price': {
                'error_messages': {
                    'invalid': '価格には有効な整数を入力してください。',
                }
            },
            'authors': {
                'error_messages': {
                    'blank': '著者は空にできません。',
                    'empty': '著者は空にできません。',
                }
            },
            'publisher': {
                'error_messages': {
                    'blank': '出版社は空にできません。',
                    'null': '出版社は空にできません。',
                }
            },
            'star': {
                'error_messages': {
                    'invalid_choice': '無効な値です。'
                }
            }
        }


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'blank': '名前は空にできません。',
                }
            },
        }


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'blank': '名前は空にできません。',
                }
            },
        }

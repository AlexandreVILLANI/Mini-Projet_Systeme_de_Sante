"""
conftest.py : Configuration globale pour Pytest avec Django.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wellmind.settings')
django.setup()


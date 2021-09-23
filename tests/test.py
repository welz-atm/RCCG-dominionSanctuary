from django.test import TestCase
from activity.forms import DonationForm, ServiceForm, TitheForm
from authentication.models import CustomUser
from activity.models import Service
import datetime
from django.urls import reverse


class ActivityFormsTestCase(TestCase):
    def setUp(self):
        user1 = CustomUser.objects.create_user(email='a@a.com', first_name='John', last_name='Good', is_admin=True,
                                               password='test123', address='Ikorodu, Lagos',
                                               telephone='+2348021234567')
        user2 = CustomUser.objects.create_user(email='a@a2.com', first_name='Johny', last_name='Goody',
                                               is_worker=True,
                                               password='test123', address='Ikorodu, Lagos',
                                               telephone='+2348021234568')
        self.service = Service.objects.create(date=datetime.date.today(), name='Sunday ThanksGiving Service',
                               announcement='Sunday school',
                               user=user1, video='C:/Users/SDSD101/Documents/GitHub/dom/DELIVERANCE FROM FREAKY FREAKY 🤣.mp4', )

    def test_correct_service_form(self):
        user = CustomUser.objects.get(id=1)
        self.client.login(email=user.email, password='test123')
        data = {
            'date': datetime.date.today(),
            'name': 'Sunday ThanksGiving Service',
            'announcement': 'Sunday school',
            'user': user.pk,
            'video': 'C:/Users/SDSD101/Documents/GitHub/dom/DELIVERANCE FROM FREAKY FREAKY 🤣.mp4',
        }
        form = ServiceForm(data=data)
        self.assertTrue(form.is_valid())

    def test_incorrect_service_form(self):
        user = CustomUser.objects.get(id=1)
        self.client.login(email=user.email, password='test123')
        data = {
            'date': datetime.date.today(),
            'name': '',
            'announcement': 'Sunday school',
            'user': user,
            'video': './DELIVERANCE FROM FREAKY FREAKY 🤣mp4',
        }
        form = ServiceForm(data=data)
        self.assertFalse(form.is_valid())

    def test_incorrect_user_service_form(self):
        user = CustomUser.objects.get(id=2)
        self.client.login(email=user.email, password='test123')
        data = {
            'date': datetime.date.today(),
            'name': '',
            'announcement': 'Sunday school',
            'user': user,
            'video': '/./m.mp4',
        }
        form = ServiceForm(data=data)
        self.assertFalse(form.is_valid())

    def test_create_service_view(self):
        user = CustomUser.objects.get(id=1)
        data = {
            'date': datetime.date.today(),
            'name': 'Sunday ThanksGiving Service',
            'announcement': 'Sunday school',
            'user': user,
            'video': '/./m.mp4',
        }
        self.client.login(email=user.email, password='test123')
        response = self.client.get(reverse('create_service'), data)
        self.assertTrue(response.status_code == 201)

    def test_correct_tithe_form(self):
        user = CustomUser.objects.get(id=1)
        self.client.login(email=user.email, password='test123')
        data = {
            'month': 'August',
            'amount': 12345,
            'user': user,
            'reference': '26yh4782dhsk',
        }
        form = TitheForm(data=data)
        self.assertFalse(form.is_valid())

    def test_incorrect_tithe_form(self):
        user = CustomUser.objects.get(id=1)
        self.client.login(email=user.email, password='test123')
        data = {
            'month': 'August',
            'amount': '',
            'user': user,
            'reference': '26yh4782dhsk',
        }
        form = TitheForm(data=data)
        self.assertFalse(form.is_valid())

    def test_pay_tithe_view(self):
        user = CustomUser.objects.get(id=1)
        self.client.login(email=user.email, password='test123')
        data = {
            'month': 'August',
            'amount': 12345,
            'user': user,
            'reference': '26yh4782dhsk',
        }
        response = self.client.post(reverse('pay_tithe'), data=data)
        self.assertTrue(response.status_code == 201)

    def test_correct_donation_form(self):
        data = {
            'amount': 12345,
            'first_name': 'Temi',
            'last_name': 'Tem',
            'email': 'tem@tem.com',
            'telephone': '+2348021234567',
            'reference': '7849hbkmdbdnd',
        }
        form = DonationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_incorrect_donation_form(self):
        data = {
            'amount': 12345,
            'first_name': 'Temi',
            'last_name': 'Tem',
            'email': '',
            'telephone': '+2348021234567',
            'reference': '7849hbkmdbdnd',
        }
        form = DonationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_make_donation_view(self):
        data = {
            'amount': 12345,
            'first_name': 'Temi',
            'last_name': 'Tem',
            'email': 'tem@tem.com',
            'telephone': '+2348021234567',
            'reference': '7849hbkmdbdnd',
        }
        response = self.client.get(reverse('make_donation'), data=data)
        self.assertTrue(response.status_code == 201)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertTrue(response.status_code == 200)

    def test_services_view(self):
        response = self.client.get(reverse('all_services'))
        self.assertTrue(response.status_code == 200)

    def test_add_image_view(self):
        service = Service.objects.get(id=1)
        response = self.client.post(reverse('add_image', kwargs={'pk': service.pk}, ))
        self.assertTrue(response.status_code == 201)

    def test_correct_registration_form(self):
        data = {
            'email': 'a@a.com',
            'first_name': 'John',
            'last_name': 'Good',
            'is_worker': True,
            'password': 'test123',
            'address': 'Ikorodu, Lagos',
            'telephone': '+2348021234567'
        }
        form = ServiceForm(data=data)
        self.assertTrue(form.is_valid())

    def test_incorrect_registration_form(self):
        data = {
            'email': 'a@a.com',
            'first_name': 'John',
            'last_name': '',
            'is_worker': True,
            'password': 'test123',
            'address': 'Ikorodu, Lagos',
            'telephone': '+2348021234567'
        }
        form = ServiceForm(data=data)
        self.assertFalse(form.is_valid())

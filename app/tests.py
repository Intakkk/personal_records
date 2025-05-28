from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import PersonalRecord

# Create your tests here.

class PersonalRecordTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass1234')
        self.user2 = User.objects.create_user(username='bob', password='pass5678')
        self.pr1 = PersonalRecord.objects.create(user=self.user1, title='Deadlift', value=120, unit='kg')
        self.pr2 = PersonalRecord.objects.create(user=self.user2, title='Squat', value=150, unit='kg')

    def test_only_user_records_are_listed(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get(reverse('pr-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Deadlift')
        self.assertNotContains(response, 'Squat')

    def test_user_can_add_pr(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.post(reverse('pr-add'), {
            'title': 'Bench Press',
            'value': 100,
            'unit': 'kg'
        })
        self.assertEqual(PersonalRecord.objects.filter(user=self.user1, title='Bench Press').count(), 1)

    def test_user_can_delete_own_pr(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.post(reverse('pr-delete', args=[self.pr1.pk]))
        self.assertEqual(PersonalRecord.objects.filter(pk=self.pr1.pk).count(), 0)

    def test_user_cannot_delete_other_user_pr(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.post(reverse('pr-delete', args=[self.pr2.pk]))
        # La vue filtre par utilisateur, donc pr2 n'existe pas pour alice → 404
        self.assertEqual(response.status_code, 404)
        self.assertEqual(PersonalRecord.objects.filter(pk=self.pr2.pk).count(), 1)

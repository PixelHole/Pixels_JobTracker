from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Application

User = get_user_model()


class ApplicationTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pw-12345-xyz")
        self.bob = User.objects.create_user("bob", password="pw-12345-xyz")
        self.alice_app = Application.objects.create(
            user=self.alice, company="Acme", position="Backend Intern"
        )
        self.bob_app = Application.objects.create(
            user=self.bob,
            company="Globex",
            position="Data Intern",
            status=Application.Status.OFFER,
        )

    def test_login_required(self):
        response = self.client.get(reverse("application-list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_list_only_shows_own_applications(self):
        self.client.login(username="alice", password="pw-12345-xyz")
        response = self.client.get(reverse("application-list"))
        self.assertContains(response, "Acme")
        self.assertNotContains(response, "Globex")

    def test_cannot_edit_or_delete_other_users_application(self):
        self.client.login(username="alice", password="pw-12345-xyz")
        edit = self.client.get(reverse("application-update", args=[self.bob_app.pk]))
        delete = self.client.post(reverse("application-delete", args=[self.bob_app.pk]))
        self.assertEqual(edit.status_code, 404)
        self.assertEqual(delete.status_code, 404)
        self.assertTrue(Application.objects.filter(pk=self.bob_app.pk).exists())

    def test_create_assigns_current_user(self):
        self.client.login(username="alice", password="pw-12345-xyz")
        self.client.post(
            reverse("application-create"),
            {
                "company": "Initech",
                "position": "Django Intern",
                "status": "applied",
                "applied_date": "2026-11-01",
            },
        )
        created = Application.objects.get(company="Initech")
        self.assertEqual(created.user, self.alice)

    def test_status_filter_and_search(self):
        self.client.login(username="alice", password="pw-12345-xyz")
        Application.objects.create(
            user=self.alice,
            company="Umbrella",
            position="QA Intern",
            status=Application.Status.REJECTED,
        )
        response = self.client.get(reverse("application-list"), {"status": "rejected"})
        self.assertContains(response, "Umbrella")
        self.assertNotContains(response, "Acme")
        response = self.client.get(reverse("application-list"), {"q": "backend"})
        self.assertContains(response, "Acme")
        self.assertNotContains(response, "Umbrella")

    def test_stats_counts(self):
        self.client.login(username="alice", password="pw-12345-xyz")
        response = self.client.get(reverse("application-list"))
        self.assertEqual(response.context["total"], 1)
        stats = {value: count for value, _, count in response.context["stats"]}
        self.assertEqual(stats["applied"], 1)
        self.assertEqual(stats["offer"], 0)

    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "carol",
                "password1": "a-strong-pass-9876",
                "password2": "a-strong-pass-9876",
            },
        )
        self.assertRedirects(response, reverse("application-list"))
        self.assertTrue(User.objects.filter(username="carol").exists())

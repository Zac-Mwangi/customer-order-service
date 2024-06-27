from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from customer_app.models import Customer
from order_app.models import Order


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create_user(
            username="john_doe",
            email="john@example.com",
            password="password123",
            code="JD123",
            phone_number="+254700000000",
        )
        self.client.force_authenticate(user=self.customer)
        self.order = Order.objects.create(
            customer=self.customer, item="Test Item", amount=100.00
        )

    def test_get_all_orders(self):
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_valid_order(self):
        response = self.client.get(
            reverse("retrieve_order", kwargs={"pk": self.order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_get_invalid_order(self):
        response = self.client.get(reverse("retrieve_order", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["success"], False)

    def test_create_valid_order(self):
        data = {"customer": self.customer.id, "item": "New Item", "amount": 200.00}
        response = self.client.post(reverse("create_order"), data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success"], True)

    def test_create_invalid_order(self):
        data = {"item": "", "amount": 200.00}
        response = self.client.post(reverse("create_order"), data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["success"], False)

    def test_update_valid_order(self):
        data = {"item": "Updated Item"}
        response = self.client.put(
            reverse("update_order", kwargs={"pk": self.order.pk}), data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

    def test_update_invalid_order(self):
        data = {"item": ""}
        response = self.client.put(
            reverse("update_order", kwargs={"pk": self.order.pk}), data, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["success"], False)

    def test_delete_valid_order(self):
        response = self.client.delete(
            reverse("delete_order", kwargs={"pk": self.order.pk})
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_invalid_order(self):
        response = self.client.delete(reverse("delete_order", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["success"], False)

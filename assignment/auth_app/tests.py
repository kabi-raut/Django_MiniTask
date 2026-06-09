from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse


class RegistrationPermissionsTests(TestCase):
	def test_register_view_assigns_editor_group_post_permissions(self):
		response = self.client.post(
			reverse('register'),
			{
				'username': 'editor_user',
				'password1': 'Strongpass123!',
				'password2': 'Strongpass123!',
			},
		)

		self.assertRedirects(response, reverse('dashboard'))

		group = Group.objects.get(name='Editor')
		user = group.user_set.get(username='editor_user')

		self.assertTrue(user.has_perm('chapter8_user_dashboard.add_userpost'))
		self.assertTrue(user.has_perm('chapter8_user_dashboard.change_userpost'))

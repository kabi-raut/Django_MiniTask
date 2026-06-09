from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from .models import UserPost


class DashboardPermissionFlowTests(TestCase):
	def setUp(self):
		self.client.post(
			reverse('chapter8_user_dashboard:register'),
			{
				'username': 'blog_user',
				'email': 'blog_user@example.com',
				'password1': 'Strongpass123!',
				'password2': 'Strongpass123!',
			},
		)
		self.user = Group.objects.get(name='blog_users').user_set.get(username='blog_user')
		self.client.login(username='blog_user', password='Strongpass123!')

	def test_registered_user_can_create_and_edit_posts(self):
		create_response = self.client.post(
			reverse('chapter8_user_dashboard:create_post'),
			{
				'title': 'First post',
				'content': 'Post content',
			},
		)

		self.assertRedirects(create_response, reverse('chapter8_user_dashboard:dashboard'))

		post = UserPost.objects.get(title='First post', user=self.user)

		edit_response = self.client.post(
			reverse('chapter8_user_dashboard:edit_post', args=[post.id]),
			{
				'title': 'Updated post',
				'content': 'Updated content',
			},
		)

		self.assertRedirects(edit_response, reverse('chapter8_user_dashboard:dashboard'))
		post.refresh_from_db()
		self.assertEqual(post.title, 'Updated post')

from django.test import TestCase
from app.models import Task
from user.models import CustomUser


class TestCreateTask(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(id=1, email='user@example.com', password='test123', first_name='User',
                                                  last_name='One',
                                                  is_active=True, is_staff=False)
        user1 = CustomUser.objects.get(id=1)
        task = Task.objects.create(id=1, task_name='django', comments='test comment', status='active', author=user1)

    def test_create_task(self):
        user = CustomUser.objects.get(id=1)
        task_in_order = Task.taskobjects.get(id=1)
        task = Task.objects.get(id=1)
        task_name = f'{task.task_name}'
        comments = f'{task.comments}'
        status = f'{task.status}'
        author = f'{user}'

        self.assertEqual(task_name, 'django')
        self.assertEqual(comments, 'test comment')
        self.assertEqual(status, 'active')
        self.assertEqual(author, str(user))
        self.assertEqual(str(task), 'django')
        self.assertEqual(str(task_in_order), 'django')

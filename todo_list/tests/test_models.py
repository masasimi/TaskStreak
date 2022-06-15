from django.test import TestCase, Client
from django.contrib.auth.models import User

from todo_list.models import Task


import datetime
from django.utils import timezone
from django.utils.timezone import localtime

class TaskModelTests(TestCase):
    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""  
        saved_tasks = Task.objects.all()
        self.assertEqual(saved_tasks.count(), 0)

'''
    def test_is_count_one(self):
        """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
        
        task = Task(title='test_title')
        task.save()
        saved_tasks = Task.objects.all()
        self.assertEqual(saved_tasks.count(), 1)

    def test_saving_and_retrieving_post(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        task = Task()
        title = 'test_title_to_retrieve'
        descirption = 'test_description_to_retrieve'
        longestStreak = 0
        currentStreak = 0
        streakSum = 0
        lastDate = localtime(timezone.now())
        isDoneToday = False

        task.title = title
        task.description = descirption
        task.longestStreak = longestStreak
        task.currentStreak = currentStreak
        task.streakSum = streakSum
        task.lastDate = lastDate
        task.isDoneToday = isDoneToday

        task.save()

        saved_tasks = Task.objects.all()
        actual_task = saved_tasks[0]

        self.assertEqual(actual_task.title, title)
        self.assertEqual(actual_task.description, descirption)
        self.assertEqual(actual_task.longestStreak, longestStreak)
        self.assertEqual(actual_task.currentStreak, currentStreak)
        self.assertEqual(actual_task.streakSum, streakSum)
        self.assertEqual(actual_task.lastDate, lastDate)
        self.assertEqual(actual_task.isDoneToday, isDoneToday)
        '''
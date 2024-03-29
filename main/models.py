from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings


class Question(models.Model):
    """
    This class is used to model questions asked by users
    It has a foreign key which corresponds to a user
    """

    title = models.CharField('title for question', max_length=150, blank=False)
    content = models.TextField(
        'more information about question', blank=True, default='')
    content_markdown = models.TextField(null=True, default='')
    asked_by = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    votes = models.IntegerField('number of votes cast', default=0)

    def __str__(self) -> str:
        return self.title[:60]

    def save_model(self, first_time=True):
        return super(Question, self).save()

    def save(self, *args, **kwargs):
        if self.id:
            super(Question, self).save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
            QuestionVote.objects.create(question=self)
            QuestionReport.objects.create(question=self)


class Answer(models.Model):
    """
    This class is used to model answers given by users to particular question.
    It has two foreign keys: 1. Question it belongs to
                             2. User who wrote it.
    """

    content = models.TextField(blank=False)
    content_markdown = models.TextField(null=True, default='')
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    answered_by = models.ForeignKey(
        to=get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.content[:60]

    def save(self, *args, **kwargs):
        if self.id:
            super(Answer, self).save(*args, **kwargs)
        else:
            super(Answer, self).save(*args, **kwargs)
            AnswerVote.objects.create(answer=self)
            AnswerReport.objects.create(answer=self)

    def save_model(self, first_time=True):
        return super(Question, self).save()


class QuestionVote(models.Model):
    """
    This model is used to store the votes casted for a particular question
    by users.

    A user can cast vote to multiple questions and a question can have votes from
    multiple users.

    A particular QuestionVote instance and a question have one-to-one relation.
    """

    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    users_downvoted = models.ManyToManyField(
        to=get_user_model(), related_name='downvotes', blank=True)
    users_upvoted = models.ManyToManyField(
        to=get_user_model(), related_name='upvotes', blank=True)
    votes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # A model should have been saved (it should have id) before accessing its
        # many-to-many fields. Below written condition will be false when object is being
        # saved for the first time. But it will run each time we update this model
        if self.id:
            updated_votes = self.users_upvoted.all().count() - \
                self.users_downvoted.all().count()
            self.votes = updated_votes

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.question} votes: {self.votes}'


class AnswerVote(models.Model):
    """
    This model is used to store the votes casted for a particular answer
    by users.

    A user can cast vote to multiple answer and an answer can have votes from
    multiple users.

    A particular AnswerVote instance and an answer have one-to-one relation.
    """

    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)
    users_downvoted = models.ManyToManyField(
        to=get_user_model(), related_name='answer_downvotes', blank=True)
    users_upvoted = models.ManyToManyField(
        to=get_user_model(), related_name='answer_upvotes', blank=True)
    votes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # A model should have been saved (it should have id) before accessing its
        # many-to-many fields. Below written condition will be false when object is being
        # saved for the first time. But it will run each time we update this model
        if self.id:
            updated_votes = self.users_upvoted.all().count() - \
                self.users_downvoted.all().count()
            self.votes = updated_votes

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.answer} votes: {self.votes}'


class Report(models.Model):
    """ This is a base class from which all classes that are used for reporting a question/answer/comment are derived.

    It provides fields common to all such as 'number_of_reports' and 'reporter' """

    # how many times this question has been flagged
    number_of_reports = models.IntegerField(default=0)

    # who has flagged this question
    reporter = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True)

    # required so that django doesn't create table for this class
    class Meta:
        abstract = True


class QuestionReport(Report):
    """ Model to store info about harmful/explicit questions """

    # which question was flagged
    question = models.OneToOneField(Question, on_delete=models.CASCADE)


class AnswerReport(Report):
    """ Model to store info about harmful/explicit answer """

    # which question was flagged
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)

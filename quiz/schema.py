import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Quiz, Category, Question, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class QuizType(DjangoObjectType):
    class Meta:
        model = Quiz
        fields = ("id", "title", "category")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz")


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text")


class Query(graphene.ObjectType):
    all_quizzes = graphene.Field(QuizType, id=graphene.Int())
    # all_questions = DjangoListField(QuestionType)

    def resolve_all_quizzes(root, info, id):
        return Quiz.objects.all().get(pk=id)

    # def resolve_all_questions(root, info):
    #     return Question.objects.all()


schema = graphene.Schema(query=Query)

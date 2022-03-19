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

class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)
    
    @classmethod
    def mutate(cls,root,info,name):
        category = Category(name=name)
        category.save()
        return CategoryMutation(category=category)


class CategoryMutationUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)
    @classmethod
    def mutate(cls, root, info, name, id):
        category= Category.objects.all().get(id=id)
        category.name=name
        category.save()
        return CategoryMutation(category=category)

class Mutation(graphene.ObjectType):
    update_category = CategoryMutation.Field()
    change_category_name = CategoryMutationUpdate.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

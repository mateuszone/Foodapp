from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from jedzonko.models import Recipe, Plan, Dayname, Recipeplan, Page
import random


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class ContactView(View):
    def get(self, request, slug):
        try:
            page = Page.objects.get(slug=slug)
        except Page.DoesNotExist:
            page = None
        ctx = {'page': page}
        return render(request, 'contact.html', ctx)



class MainView(View):

    def get(self, request):
        try:
            page = Page.objects.get(slug="contact")
        except Page.DoesNotExist:
            page = None
        results = Recipe.objects.all()
        results = [x for x in results]
        random.shuffle(results)
        results = results[:3]
        ctx = {'results': results, 'page': page}
        about_page = Page.objects.get(slug="about") if Page.objects.filter(slug="about").exists() else None
        ctx['about_page'] = about_page
        return render(request, 'index.html', ctx)


class DashboardView(View):
    def get(self, request):
        plans_counter = Plan.objects.all().count()
        recipes = Recipe.objects.all()
        latest_plan = Plan.objects.latest('created')
        days = [x.day_name.order for x in latest_plan.recipeplan_set.all()]
        days = set(days)
        counter = 0
        for recipe in recipes:
            counter += 1
        ctx = {
            'counter': counter, "plans_counter": plans_counter, "latest_plan": latest_plan,
            "days": days,
        }
        return render(request, "dashboard.html", ctx)


class RecipeDetailView(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        ctx = {'recipe': recipe}
        return render(request, "app-recipe-details.html", ctx)

    def post(self, request, id):
        recipe = Recipe.objects.get(id=id)
        up = request.POST.get("up")
        down = request.POST.get("down")
        if up:
            recipe.votes += 1
            recipe.save()
        if down:
            recipe.votes -= 1
            recipe.save()
        return redirect("recipe_detail", id=recipe.id)


class RecipeListView(View):
    def get(self, request):
        recipe_list = Recipe.objects.order_by('-votes', '-created')
        paginator = Paginator(recipe_list, 50)  # tu można zmienić liczbę przepisów ustawianych na stronie
        page = request.GET.get('page', 1)
        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            recipes = paginator.page(1)
        except EmptyPage:
            recipes = paginator.page(paginator.num_pages)

        return render(request, "app-recipes.html", {'recipes': recipes})


class RecipeSearchView(View):
    def get(self, request):
        name = request.GET.get("search_name")
        recipes = Recipe.objects.filter(name__icontains=name)
        return render(request, "app-recipes.html", {'recipes': recipes})


class RecipeAddView(View):
    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        name = request.POST['recipeName']
        ingredients = request.POST['ingredients']
        description = request.POST['recipeDescription']
        preparation_time = request.POST['preparation']
        directions = request.POST['way0fPreparation']
        if name and ingredients and description and preparation_time and directions:
            new_recipe = Recipe.objects.create(name=name, ingredients=ingredients, description=description,
                                               preparation_time=preparation_time, directions=directions)

            return redirect('recipe_list')
        else:
            error = "Wypełnij poprawnie wszystkie pola"
            return render(request, "app-add-recipe.html", {'error': error})


class RecipeModifyView(View):

    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        return render(request, "app-edit-recipe.html", {'recipe': recipe})

    def post(self, request, id):
        name = request.POST.get('recipeName')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        directions = request.POST.get('directions')
        ingredients = request.POST.get('ingredients')
        if name and description and preparation_time and directions and ingredients:
            Recipe.objects.create(name=name, ingredients=ingredients, description=description,
                                  preparation_time=preparation_time, directions=directions)
            return redirect("recipe_list")
        else:
            recipe = Recipe(name=name, ingredients=ingredients, description=description,
                            preparation_time=preparation_time, directions=directions)
            error = "Wypełnij poprawnie wszystkie pola"
            ctx = {'recipe': recipe, 'error': error}
            return render(request, "app-edit-recipe.html", ctx)


class RecipeDeleteView(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        recipe.delete()
        return redirect('recipe_list')

class PlanDetailView(View):
    def get(self, request, id):
        plan = Plan.objects.get(pk=id)
        ctx = {
            "plan": plan,
        }
        return render(request, "app-details-schedules.html", ctx)


class PlanListView(View):
    def get(self, request):
        plans_list = Plan.objects.order_by('name')
        paginator = Paginator(plans_list, 50)
        page = request.GET.get('page', 1)
        try:
            plans = paginator.page(page)
        except PageNotAnInteger:
            plans = paginator.page(1)
        except EmptyPage:
            plans = paginator.page(paginator.num_pages)
        return render(request, "app-schedules.html", {"plans": plans})


class PlanAddView(View):
    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get('planName')
        description = request.POST.get('planDesc')

        if not name or not description:
            ctx = {'Error': 'Plan name, description or both are empty'}
            return render(request, "app-add-schedules.html", ctx)

        p = Plan()
        p.name = name
        p.description = description
        p.save()
        return redirect('plan_detail', id=p.id)


class PlanAddRecipeView(View):
    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = Dayname.objects.all()
        ctx = {'plans': plans, 'recipes': recipes, 'days': days}
        return render(request, "app-schedules-meal-recipe.html", ctx)

    def post(self, request):
        plan_id = request.POST.get('choosePlan')
        plan = Plan.objects.get(pk=plan_id)
        meal_name = request.POST.get('name')
        order = request.POST.get('order')
        day_order = int(request.POST.get('day'))
        day = Dayname.objects.get(order=day_order)
        recipe_id = request.POST.get('recipe')
        recipe = Recipe.objects.get(pk=recipe_id)

        Recipeplan.objects.create(meal_name=meal_name, order=order, day_name=day, plan=plan, recipe=recipe)
        return redirect('plan_detail', id=plan.id)


class AboutPageView(View):
    def get(self, request):

        about_page = Page.objects.get(slug="about") if Page.objects.filter(slug="about").exists() else None   
        contact_page = Page.objects.get(slug="contact") if Page.objects.filter(slug="contact").exists() else None
        return render(request, "about.html", {"page": about_page, "contact_page": contact_page})

class PlanModifyView(View):
    def get(self, request, id):
        plan = get_object_or_404(Plan, pk=id)
        return render(request, "app-edit-schedules.html", {'plan': plan})

    def post(self, request, id):
        name = request.POST.get('planName')
        description = request.POST.get('planDesc')
        if name and description:
            Plan.objects.create(name=name, description=description,)
            return redirect("plan_list")
        else:
            plan = Plan(name=name, description=description)
            error = "Wypełnij poprawnie wszystkie pola"
            ctx = {'plan': plan, 'error': error}
            return render(request, "app-edit-schedules.html", ctx)


class PlanDeleteView(View):
    def get(self, request, id):
        plan = get_object_or_404(Plan, id=id)
        plan.delete()
        return redirect('plan_list')

class RecipePlanDeleteView(View):
    def get(self, request, plan_id, recipeplan_id):
        recipeplan = get_object_or_404(Recipeplan, id=recipeplan_id)
        recipeplan.delete()
        return redirect('plan_detail', plan_id)


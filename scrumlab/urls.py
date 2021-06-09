"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Functigit staon views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path



from jedzonko.views import (IndexView, DashboardView, MainView, RecipeDetailView, RecipeListView, RecipeAddView, 
                            RecipeModifyView, PlanDetailView, PlanListView, PlanAddView, PlanAddRecipeView, AboutPageView, ContactView,
                            PlanModifyView, PlanDeleteView, RecipeDeleteView, RecipeSearchView, RecipePlanDeleteView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', MainView.as_view()),
    path('main/', DashboardView.as_view(), name='main'),
    path('contact/<slug:slug>/', ContactView.as_view(), name='contact'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('recipe/<int:id>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/list/', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/add/', RecipeAddView.as_view(), name='recipe_add'),
    path('recipe/modify/<int:id>/', RecipeModifyView.as_view(), name='recipe_modify'),
    path('plan/<int:id>/', PlanDetailView.as_view(), name='plan_detail'),
    path('plan/list/', PlanListView.as_view(), name='plan_list'),
    path('plan/add/', PlanAddView.as_view(), name='plan_add'),
    path('plan/add-recipe/', PlanAddRecipeView.as_view(), name='plan_add_recipe'),
    path('plan/modify/<int:id>/', PlanModifyView.as_view(), name='plan_modify'),
    path('plan/<int:id>/delete/', PlanDeleteView.as_view(), name='plan_delete'),
    path('recipe/delete/<int:id>/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('recipe/search/', RecipeSearchView.as_view(), name='search'),
    path('plan/<int:plan_id>/delete_recipeplan/<int:recipeplan_id>/', RecipePlanDeleteView.as_view(), name='recipeplan_delete')
]

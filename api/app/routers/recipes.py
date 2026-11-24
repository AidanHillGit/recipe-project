from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models import Recipe, User
from app.schemas import RecipeCreate, RecipeRead

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=RecipeRead)
def create_recipe(
    recipe_in: RecipeCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Create a recipe owned by the logged-in user."""
    recipe = Recipe(
        title=recipe_in.title,
        description=recipe_in.description,
        servings=recipe_in.servings,
        total_minutes=recipe_in.total_minutes,
        owner_id=current_user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.get("", response_model=list[RecipeRead])
def list_recipes(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Return the logged-in user's recipes, newest first."""
    query = (
        select(Recipe)
        .where(Recipe.owner_id == current_user.id)
        .order_by(Recipe.created_at.desc())
    )
    recipes = db.scalars(query).all()
    return recipes


@router.get("/{recipe_id}", response_model=RecipeRead)
def read_recipe(
    recipe_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Return one of the logged-in user's recipes, or 404."""
    recipe = db.get(Recipe, recipe_id)
    if recipe is None or recipe.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Delete one of the logged-in user's recipes, or 404."""
    recipe = db.get(Recipe, recipe_id)
    if recipe is None or recipe.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )
    db.delete(recipe)
    db.commit()

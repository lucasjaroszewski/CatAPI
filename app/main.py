from fastapi import FastAPI, Response, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


class Cat(BaseModel):
    breed: str
    location_of_origin: str
    coat_length: int
    body_type: str
    pattern: str


cats = [
    {
        'breed': 'Siamese',
        'location_of_origin': 'Thailand',
        'coat_length': 4,
        'body_type': 'Medium',
        'pattern': 'Chocolate Point'
    },
    {
        'breed': 'Persian',
        'location_of_origin': 'Iran',
        'coat_length': 4,
        'body_type': 'Medium',
        'pattern': 'White and Black'
    }
]


@app.get("/cats", response_model=List[Cat])
async def get_cats(breed: Optional[str] = Query(None),
                   location_of_origin: Optional[str] = Query(None),
                   coat_length: Optional[int] = Query(None, ge=0),
                   body_type: Optional[str] = Query(None),
                   pattern: Optional[str] = Query(None)):

    if breed:
        return [cat for cat in cats if cat["breed"] == breed]

    if location_of_origin:
        return [cat for cat in cats if cat["location_of_origin"] == location_of_origin]

    if coat_length:
        return [cat for cat in cats if cat["coat_length"] == coat_length]

    if body_type:
        return [cat for cat in cats if cat["body_type"] == body_type]

    if pattern:
        return [cat for cat in cats if cat["pattern"] == pattern]

    return cats


@app.post("/cats", status_code=status.HTTP_201_CREATED)
async def create_cat(cat: Cat):
    cats.append(cat.dict())
    return cat


@app.put("/cats/{cat_breed}", status_code=status.HTTP_202_ACCEPTED)
async def update_cat(cat_breed: str, cat: Cat):
    for cat in cats:
        if (cat.breed == cat_breed):
            return cats.update(cat)

    return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/cats/{cat_breed}")
async def delete_cat(cat_breed: str):
    for cat in cats:
        if (cat.breed == cat_breed):
            return cats.remove(cat)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

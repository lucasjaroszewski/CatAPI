from fastapi import FastAPI, Response, Query, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
import logging

# Logging Configuration
logging.basicConfig(filename='CatAPI.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# FastAPI Configuration
app = FastAPI()

# Models Configuration
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


# CRUD Configuration
@app.get("/cats", response_model=List[Cat], status_code=status.HTTP_200_OK)
async def get_cats(breed: Optional[str] = Query(None),
                   location_of_origin: Optional[str] = Query(None),
                   coat_length: Optional[int] = Query(None, ge=0),
                   body_type: Optional[str] = Query(None),
                   pattern: Optional[str] = Query(None)):

    if breed:
        logging.info('Querying all cats that have {} as breed.'.format(breed))
        return [cat for cat in cats if cat["breed"] == breed]

    if location_of_origin:
        logging.info('Querying all cats that have {} as location of origin.'.format(location_of_origin))
        return [cat for cat in cats if cat["location_of_origin"] == location_of_origin]

    if coat_length:
        logging.info('Querying all cats that have {} as coat length.'.format(coat_length))
        return [cat for cat in cats if cat["coat_length"] == coat_length]

    if body_type:
        logging.info('Querying all cats that have {} as body type.'.format(body_type))
        return [cat for cat in cats if cat["body_type"] == body_type]

    if pattern:
        logging.info('Querying all cats that have {} as pattern.'.format(pattern))
        return [cat for cat in cats if cat["pattern"] == pattern]

    return cats


@app.post("/cats", status_code=status.HTTP_201_CREATED)
async def add_cat(cat: Cat,
                  breed: str,
                  location_of_origin: str,
                  coat_length: int,
                  body_type: str,
                  pattern: str):

    new_cat = cat.dict()
    new_cat['breed'] = breed

    if [cat for cat in cats if cat["breed"] == breed]:
        logging.warning('Breed already exists.')
        raise HTTPException(status_code=406, detail="Breed already exists.")

    new_cat['location_of_origin'] = location_of_origin
    new_cat['coat_length'] = coat_length

    if coat_length < 0:
        logging.warning('Coat length must be equal or greater than 0.')
        raise HTTPException(status_code=406, detail="Coat length must be equal or greater than 0.")

    new_cat['body_type'] = body_type
    new_cat['pattern'] = pattern
    cats.append(new_cat)

    logging.info('Added {} cat from {}, with {} coat length, {} body type and {} pattern.'.format(breed, new_cat['location_of_origin'], new_cat['coat_length'], new_cat['body_type'], new_cat['pattern']))
    return new_cat


@app.put("/cats/{breed}", status_code=status.HTTP_202_ACCEPTED)
async def update_cat(breed: str, cat: Cat):
    for cat in cats:
        if (cat.breed == breed):
            return cats.update(cat)

    return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/cats/{breed}")
async def delete_cat(breed: str):
    for cat in cats:
        if (cat.breed == breed):
            return cats.remove(cat)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

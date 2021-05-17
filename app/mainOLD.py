from fastapi import FastAPI, Response, Query, HTTPException, status
from fastapi.encoders import jsonable_encoder
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
    breed = breed.capitalize()
    new_cat['breed'] = breed

    if [cat for cat in cats if cat["breed"] == breed]:
        logging.error('Breed already exists.')
        raise HTTPException(status_code=406, detail="Breed already exists.")

    location_of_origin = location_of_origin.capitalize()
    new_cat['location_of_origin'] = location_of_origin
    new_cat['coat_length'] = coat_length

    if coat_length < 0:
        logging.error('Coat length must be equal or greater than 0.')
        raise HTTPException(status_code=406, detail="Coat length must be equal or greater than 0.")

    body_type = body_type.capitalize()
    new_cat['body_type'] = body_type

    body_types = ['Small', 'Medium', 'Large']
    if body_type not in body_types:
        logging.error('Body type must be Small, Medium or Large')
        raise HTTPException(status_code=406, detail="Body type must be Small, Medium or Large")

    pattern = pattern.capitalize()
    new_cat['pattern'] = pattern

    cats.append(new_cat)
    logging.info('Added {} cat from {}, with {} coat length, {} body type and {} pattern.'.format(breed, new_cat['location_of_origin'], new_cat['coat_length'], new_cat['body_type'], new_cat['pattern']))
    return new_cat


@app.patch("/cats/{breed}", response_model=Cat, status_code=status.HTTP_202_ACCEPTED)
async def update_cat(cat: Cat,
                     breed: str,
                     location_of_origin: str,
                     coat_length: int,
                     body_type: str,
                     pattern: str):

    update_cat = cat.dict()

    for cat in cats:
        if cat['breed'] == breed:

            breed = breed.capitalize()
            update_cat['breed'] = breed

            location_of_origin = location_of_origin.capitalize()
            update_cat['location_of_origin'] = location_of_origin

            update_cat['coat_length'] = coat_length
            if coat_length < 0:
                logging.error('Coat length must be equal or greater than 0.')
                raise HTTPException(status_code=406, detail="Coat length must be equal or greater than 0.")

            body_type = body_type.capitalize()
            update_cat['body_type'] = body_type

            body_types = ['Small', 'Medium', 'Large']
            if body_type not in body_types:
                logging.error('Body type must be Small, Medium or Large')
                raise HTTPException(status_code=406, detail="Body type must be Small, Medium or Large")

            pattern = pattern.capitalize()
            update_cat['pattern'] = pattern

            cats.update(update_cat)
            logging.info('Updated {} cat from {}, with {} coat length, {} body type and {} pattern.'.format(breed, update_cat['location_of_origin'], update_cat['coat_length'], update_cat['body_type'], update_cat['pattern']))
            return update_cat
    else:
        logging.warning('Cat not found.')
        raise HTTPException(status_code=404, detail="Cat not found")




@app.delete("/cats/{breed}")
async def delete_cat(breed: str):
    for cat in cats:
        if (cat.breed == breed):
            return cats.remove(cat)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

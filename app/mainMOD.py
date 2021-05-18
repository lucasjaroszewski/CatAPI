from fastapi import FastAPI, Query, HTTPException, status
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
@app.post("/cats", status_code=status.HTTP_201_CREATED)
async def add_cat(new_cat: Cat,
                  breed: Optional[str] = None,
                  location_of_origin: Optional[str] = None,
                  coat_length: Optional[int] = None,
                  body_type: Optional[str] = None,
                  pattern: Optional[str] = None):

    if new_cat.breed:
        new_cat.breed = new_cat.breed.capitalize()
        print('oie')

    if [cat for cat in cats if cat["breed"] == new_cat.breed]:
        logging.error('Breed already exists.')
        raise HTTPException(status_code=406, detail="Breed already exists.")

    cats.append(new_cat)
    # logging.info('Added {} cat from {}, with {} coat length, {} body type and {} pattern.'.format(breed, cat['location_of_origin'], cat['coat_length'], cat['body_type'], cat['pattern']))
    return new_cat

#    if location_of_origin:
#        location_of_origin = location_of_origin.capitalize()
#        cat['location_of_origin'] = location_of_origin
#
#    if coat_length:
#        cat['coat_length'] = coat_length
#        if coat_length < 0:
#            logging.error('Coat length must be equal or greater than 0.')
#            raise HTTPException(status_code=406, detail="Coat length must be equal or greater than 0.")
#
#    if body_type:
#        body_type = body_type.capitalize()
#        cat['body_type'] = body_type
#        body_types = ['Small', 'Medium', 'Large']
#        if body_type not in body_types:
#            logging.error('Body type must be Small, Medium or Large')
#            raise HTTPException(status_code=406, detail="Body type must be Small, Medium or Large")
#
#    if pattern:
#        pattern = pattern.capitalize()
#        cat['pattern'] = pattern


@app.post("/cats", status_code=status.HTTP_201_CREATED)
async def add_cat(cat: Cat):

    print('breed', cat.breed)
    print('location_of_origin', cat.location_of_origin)
    for i in cats:
        if str(cat.breed) == str(i['breed']):
            print('o loquinho meu')


    cats.append(cat)
    #logging.info('Added {} cat from {}, with {} coat length, {} body type and {} pattern.'.format(breed, new_cat['location_of_origin'], new_cat['coat_length'], new_cat['body_type'], new_cat['pattern']))
    return cat


@app.patch("/cats/{breed}", response_model=Cat, status_code=status.HTTP_202_ACCEPTED)
async def update_cat(cat: Cat,
                     breed: str,
                     location_of_origin: str = None,
                     coat_length: int = None,
                     body_type: str = None,
                     pattern: str = None):

    for cat in cats:
        if cat['breed'] == breed:
            update_cat = cat

            if location_of_origin:
                location_of_origin = location_of_origin.capitalize()
                logging.info('Cat of {} breed - Updated location of origin: {}'.format(breed, location_of_origin))
                update_cat['location_of_origin'] = location_of_origin

            if coat_length:
                update_cat['coat_length'] = coat_length
                if coat_length < 0:
                    logging.error('Coat length must be equal or greater than 0.')
                    raise HTTPException(status_code=406, detail="Coat length must be equal or greater than 0.")
                logging.info('Cat of {} breed - Updated coat length: {}'.format(breed, coat_length))

            if body_type:
                body_type = body_type.capitalize()
                update_cat['body_type'] = body_type
                body_types = ['Small', 'Medium', 'Large']

                if body_type not in body_types:
                    logging.error('Body type must be Small, Medium or Large')
                    raise HTTPException(status_code=406, detail="Body type must be Small, Medium or Large")
                logging.info('Cat of {} breed - Updated body type: {}'.format(breed, body_type))

            if pattern:
                pattern = pattern.capitalize()
                update_cat['pattern'] = pattern
                logging.info('Cat of {} breed - Updated pattern: {}'.format(breed, pattern))

            return update_cat

        else:
            raise HTTPException(status_code=404, detail="Cat not found.")


@app.delete("/cats/{breed}")
async def delete_cat(breed: str):

    for cat in cats:
        if cat['breed'] == breed:
            return cats.remove(cat)

        else:
            raise HTTPException(status_code=404, detail="Cat not found.")


# POST request of three cats
@app.post("/add_three_cats", status_code=status.HTTP_201_CREATED)
async def add_three_cats(cat: Cat):
    await add_cat(cat, 'Bengal', 'United States', 1, 'Large', 'Orange')
    await add_cat(cat, 'Maine Coon', 'United States', 3, 'Large', 'Brown Tabby')
    await add_cat(cat, 'Peterbald', 'Russia', 0, 'Small', 'Grey')
    logging.info('Cats added successfully.')

    return {'status': 'http_201_created'}

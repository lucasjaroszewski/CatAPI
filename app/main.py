from fastapi import FastAPI, HTTPException, status
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


# Initial Cat Database
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
async def get_cats(breed: Optional[str] = None,
                   location_of_origin: Optional[str] = None,
                   coat_length: Optional[int] = None,
                   body_type: Optional[str] = None,
                   pattern: Optional[str] = None):

    # Query: Only show cats with the same breed
    if breed:
        logging.info('Querying all cats that have {} as breed.'.format(breed))
        return [cat for cat in cats if cat["breed"] == breed]

    # Query: Only show cats with the same location of origin
    if location_of_origin:
        logging.info('Querying all cats that have {} as location of origin.'.format(location_of_origin))
        return [cat for cat in cats if cat["location_of_origin"] == location_of_origin]

    # Query: Only show cats with the same coat length
    if coat_length:
        logging.info('Querying all cats that have {} as coat length.'.format(coat_length))
        return [cat for cat in cats if cat["coat_length"] == coat_length]

    # Query: Only show cats with the same body type
    if body_type:
        logging.info('Querying all cats that have {} as body type.'.format(body_type))
        return [cat for cat in cats if cat["body_type"] == body_type]

    # Query: Only show cats with the same pattern
    if pattern:
        logging.info('Querying all cats that have {} as pattern.'.format(pattern))
        return [cat for cat in cats if cat["pattern"] == pattern]

    # If no query was input, show all cats
    return cats


@app.post("/cats", response_model=Cat, status_code=status.HTTP_201_CREATED)
async def add_cat(new_cat: Cat):

    # Update entries to check validations
    new_cat.breed = new_cat.breed.title()
    new_cat.location_of_origin = new_cat.location_of_origin.title()
    new_cat.body_type = new_cat.body_type.capitalize()
    new_cat.pattern = new_cat.pattern.title()

    # Validation: Check if breed is unique
    if [cat for cat in cats if cat["breed"] == (new_cat.breed)]:
        logging.error('Breed already exists.')
        raise HTTPException(status_code=406, detail="Breed already exists.")

    # Validation: Check if coat length is a positive integer
    if (new_cat.coat_length) < 0:
        logging.error('Coat length must be equal or greater than 0.')
        raise HTTPException(status_code=406, detail="Coat length must be equal or greater than 0.")

    # Validation: Check if body type matches with predefined values
    body_types = ['Small', 'Medium', 'Large']
    if (new_cat.body_type) not in body_types:
        logging.error('Body type must be Small, Medium or Large')
        raise HTTPException(status_code=406, detail="Body type must be Small, Medium or Large")

    cats.append(new_cat.dict())
    logging.info('{} created successfully!'.format((new_cat.breed)))
    return new_cat


@app.patch("/cats/{breed}", response_model=Cat, status_code=status.HTTP_202_ACCEPTED)
async def update_cat(breed: str, query_cat: Cat):

    # Validation: Check if breed is NOT unique
    for cat in cats:
        if cat['breed'] == breed:

            # Validation: Check if there is a location of origin to update
            if query_cat.location_of_origin:
                cat['location_of_origin'] = query_cat.location_of_origin.title()
                logging.info('Cat of {} breed - Updated location of origin: {}'.format(breed, (query_cat.location_of_origin)))

            # Validation: Check if there is a positive integer coat length to update
            if query_cat.coat_length:
                cat['coat_length'] = query_cat.coat_length
                if (query_cat.coat_length) < 0:
                    logging.error('Coat length must be equal or greater than 0.')
                    raise HTTPException(status_code=406, detail="Coat length must be equal or greater than 0.")
                logging.info('Cat of {} breed - Updated coat length: {}'.format(breed, (query_cat.coat_length)))

            # Validation: Check if there is a valid body type to update
            if query_cat.body_type:
                cat['body_type'] = query_cat.body_type.capitalize()
                body_types = ['Small', 'Medium', 'Large']

                if query_cat.body_type.capitalize() not in body_types:
                    logging.error('Body type must be Small, Medium or Large')
                    raise HTTPException(status_code=406, detail="Body type must be Small, Medium or Large")
                logging.info('Cat of {} breed - Updated body type: {}'.format(breed, (query_cat.body_type)))

            # Validation: Check if there is a pattern to update
            if query_cat.pattern:
                cat['pattern'] = query_cat.pattern.title()
                logging.info('Cat of {} breed - Updated pattern: {}'.format(breed, (query_cat.pattern)))

            return cat

    else:
        raise HTTPException(status_code=404, detail="Cat not found.")


@app.delete("/cats/{breed}")
async def delete_cat(breed: str):

    # Validation: Check if the breed exists
    for cat in cats:
        if cat['breed'] == breed:
            return cats.remove(cat)

    else:
        raise HTTPException(status_code=404, detail="Cat not found.")


# POST request of three cats
@app.post("/add_three_cats", status_code=status.HTTP_201_CREATED)
async def add_three_cats(cat: Cat):
    await add_cat(Cat(breed='Bengal', location_of_origin='United States', coat_length=1, body_type='Large', pattern='Orange'))
    await add_cat(Cat(breed='Maine Coon', location_of_origin='United States', coat_length=3, body_type='Large', pattern='Brown Tabby'))
    await add_cat(Cat(breed='Peterbald', location_of_origin='United States', coat_length=0, body_type='Small', pattern='Grey'))

    logging.info('Cats added successfully.')
    return {'status': 'http_201_created'}

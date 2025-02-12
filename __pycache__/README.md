# Fresh Fruit Inventory API

## Overview
This API manages a fresh fruit inventory system. It supports CRUD operations for fruits, including adding, updating, retrieving, and "deleting" (setting availability to false) fruits.

## Endpoints
1. **GET /api/fruits**: Retrieve all available fruits.
2. **GET /api/fruits/{id}**: Retrieve details of a specific fruit.
3. **POST /api/fruits**: Add a new fruit to the inventory.
4. **PATCH /api/fruits/{id}**: Update a fruit's availability, price, or quantity.
5. **DELETE /api/fruits/{id}**: Set a fruit's availability to false.

## Screenshots

# GET All Fruits
[GET All Fruits](get_all_fruits.png)
# GET Specific Fruits 
[Get specific fruit] (get_specific_fruit.png)

### POST New Fruit
![POST New Fruit](post_new_fruit.png)

### PATCH Update Fruit
![PATCH Update Fruit](patch_update_fruit.png)

!testing that a deleted fruit is false(proving that pacth cannot be done a deleted fruit.png)

### DELETE Fruit
![DELETE Fruit](delete_fruit.png)
testing that deleted fruit is now unavailable.png
import mysql.connector
import getpass
from datetime import datetime

us = 'token_55ca'
pw = 'WKN024EcbaETnZg5'
try:
    cnx = mysql.connector.connect(

        user=us,
        password=pw,
        host='127.0.0.1',
        database='bth0331_Final_Project'
    )
    cursor  = cnx.cursor(buffered=True)
    
    def createRecipe():
        #prompt user for everything
        recipeName = input("Enter name of recipe\n")
        cookTime = input("Enter time in whole minutes\n")
        int(cookTime)
        servingSize = input("How many people does it serve?\n")
        int(servingSize)
        description = input("Enter a short description of the recipe\n")
        instructions = input("Enter the instructions for your recipe\n")
        categoryMenu = """
        What category does your recipe belong to?
        1.Appetizers
        2.Beverages
        3.Breads
        4.Desserts
        5.Main Dishes
        6.Miscellaneous
        7.Salads
        8.Soups
        9.Vegetables
        """
        command = input(categoryMenu)
        if (command == "1"):
            category = "Appetizers"
        elif (command == "2"):
            category = "Beverages"
        elif (command == "3"):
            category = "Breads"
        elif (command == "4"):
            category = "Desserts"
        elif (command == "5"):
            category = "Main Dishes"
        elif (command == "6"):
            category = "Miscellaneous"
        elif (command == "7"):
            category = "Salads"
        elif (command == "8"):
            category = "Soups"
        elif (command == "9"):
            category = "Vegetables"
        
        dietaryTags = """
        Does your recipe have any dietary tags you'd like to add?
        1.Vegetarian
        2.Vegan
        3.Gluten-Free
        4.Sugar-Free
        5.None
        """
        command = input(dietaryTags)
        if (command == "1"):
            tags = "Vegetarian"
        elif (command == "2"):
            tags = "Vegan"
        elif (command == "3"):
            tags = "Gluten-Free"
        elif (command == "4"):
            tags = "Sugar-Free"
        elif (command == "5"):
            tags = "None"
        
        countryOfOrigin = """
        Input continent of origin for your recipe:
        1.Africa
        2.Asia
        3.Europe
        4.North America
        5.South America
        6.Antarctica
        7.Australia 
        """
        country = ""
        origin = input(countryOfOrigin)
        if(origin == "1"):
            country = "Africa"
        elif (origin == "2"):
            country = "Asia"
        elif (origin == "3"):
            country = "Europe"
        elif (origin == "4"):
            country = "North America"
        elif (origin == "5"):
            country = "South America"
        elif (origin == "6"):
            country == "Antarctica"
        elif (origin == "7"):
            country == "Australia"

        ingredients = {}
        foodType = ""
        decision = "0"
        while(decision != '1'):
            temp = input("input name of ingredient ")
            foodTypeMenu = """
            What food type does it belong to?
            1.Dairy
            2.Fruit
            3.Grain
            4.Protein
            5.Starch
            6.Vegetable
            """
            tempNumber = input(foodTypeMenu)
            if (tempNumber == "1"):
                foodType = "Dairy"
            elif (tempNumber == "2"):
                foodType = "Fruit"
            elif (tempNumber == "3"):
                foodType = "Grain"
            elif (tempNumber == "4"):
                foodType = "Protein"
            elif (tempNumber == "5"):
                foodType = "Starch"
            elif (tempNumber == "6"):
                foodType = "Vegetable"
            ingredients[temp] = foodType
            decision = input("""
            Are you done inputing ingredients?
            1.Yes 
            2.No
            """)
        email = input("Enter your email\n")

        query = f"""INSERT IGNORE INTO FoodType
            (type)
            VALUES
            (%s)
        """
        cursor.execute(query, (category,))

        query = f"""SELECT FoodType.type FROM FoodType 
        """
        cursor.execute(query)
        for f in cursor:
            print(f)

        query = f"""INSERT IGNORE INTO Origin
            (name)
            VALUES
            (%s) 
        """
        cursor.execute(query, (country,))
        # This query is extremely sus
        # It passes through but it doesn't add anything to our DB
        # No Syntax Errors, but when the query is executed below it doesn't
        # do anything and fails at another query.   
        
        query = f"""INSERT INTO Recipe
            (originId, foodTypeId, userId, title, cookTime, servingSize, description, instructions)
            SELECT Origin.id, FoodType.id, User.id, %s, %s, %s, %s, %s
            FROM Origin, FoodType, User 
            WHERE Origin.name = %s
            AND FoodType.type = %s   
            AND User.email = %s
        """
        print(recipeName)
        print(cookTime)
        print(servingSize)
        print(description)
        print(instructions)
        print(country)
        print(category)
        print(email)
        cursor.execute(query, (recipeName, cookTime, servingSize, description, instructions, country, category, email,))
        
        query = f"""SELECT Recipe.title FROM Recipe 
        """
        cursor.execute(query)
        for r in cursor:
            print(r)
        
        query = f"""INSERT INTO Access
        (userId, recipeId)
        SELECT User.id, Recipe.id 
        FROM User, Recipe
        WHERE User.email = %s
        AND Recipe.title = %s
        """
        cursor.execute(query, (email, recipeName,))

        for ingredient in ingredients:
            print(ingredient)
            print(ingredients[ingredient])
            query = f"""INSERT IGNORE INTO Ingredient
            (name, foodGroup)
            VALUES
            (%s, %s)
            """
            cursor.execute(query, (ingredient, ingredients[ingredient]))
            print("executed ingredient forloop")
        
        query = f"""SELECT Ingredient.name FROM Ingredient 
        """
        cursor.execute(query)
        for i in cursor:
            print(i)
            
        query = f"""SELECT title FROM Recipe 
        """
        cursor.execute(query)
        for r in cursor:
            print(r)
        for ingredient in ingredients:
            print("in comprise")
            
            query = f"""INSERT IGNORE INTO Comprise
            (recipeId, ingredientId)
            SELECT Recipe.id, Ingredient.id
            FROM Recipe, Ingredient
            WHERE Recipe.title = %s
            AND Ingredient.name = %s
            """
            cursor.execute(query, (recipeName, ingredient,))
            print("executed comprise")
    command = ""
    done = False
    while done !=  True:
        topMenu = """
        1.Create recipe
        2.Search
        3.New User
        4.Quit
        """
        command = input(topMenu)
        if command == "1":
            # are you a user?
            createRecipe()
            query = f"""SELECT Recipe.title
            FROM Recipe
            """
            cursor.execute(query)
            for recipe in cursor:
                print(recipe)

        elif command == "2":
            searchMenu = """
            1.Search by recipe
            2.Search by user
            3.Back
            """
            
            command = input(searchMenu)
            if(command == "1"):
                searchRecipeMenu = """
                1.Search by category
                2.Search by keyword
                3.Back
                """
                command = input(searchRecipeMenu)
                if(command == "1"):
                    categoryMenu = """
                    Which catergory would you like to search
                    1.Appetizer
                    2.Beverage
                    3.Breads
                    4.Desserts
                    5.Main Dishes
                    6.Miscellaneous
                    7.Salads
                    8.Soups
                    9.Vegetables
                    """
                    query = f"""
                        Select Recipe.title, Recipe.cookTime, Recipe.servingSize, Recipe.description, Recipe.instructions, Origin.name, FoodType.type, User.fName, User.lName
                        FROM Recipe
                            INNER JOIN Origin ON Recipe.originId = Origin.id
                            INNER JOIN FoodType ON Recipe.foodTypeId = FoodType.id
                            INNER JOIN User ON Recipe.userId = User.id
                        WHERE FoodType.type = %s;
                        """
                    command = input(categoryMenu)
                    if (command == "1"):
                        category = "Appetizer"
                        cursor.execute(query, (category,))
                    elif (command == "2"):
                        category = "Beverage"
                        cursor.execute(query, (category,))
                    elif (command == "3"):
                        category = "Breads"
                        cursor.execute(query, (category,))
                    elif (command == "4"):
                        category = "Desserts"
                        cursor.execute(query, (category,))
                    elif (command == "5"):
                        category = "Main Dishes"
                        cursor.execute(query, (category,))
                    elif (command == "6"):
                        category = "Miscellaneous"
                        cursor.execute(query, (category,))
                    elif (command == "7"):
                        category = "Salads"
                        cursor.execute(query, (category,))
                    elif (command == "8"):
                        category = "Soups"
                        cursor.execute(query, (category,))
                    elif (command == "9"):
                        category = "Vegetables"
                        cursor.execute(query, (category,))
                    for(title, cookTime, servingSize, description, instructions, originName, type, fName, lName) in cursor:
                        print(f"Recipe Name: {title} Cook Time: {cookTime} Serving Size: {servingSize} Description: {description} Instructions: {instructions} Country of Origin: {originName}, Type: {type} User: {fName} {lName}")
                elif(command == "2"):
                    keyword = input("Enter keyword to search by: ")
                    query = f"""
                    Select Recipe.title, Recipe.cookTime, Recipe.servingSize, Recipe.description, Recipe.instructions, Origin.name, FoodType.type, User.fName, User.lName
                        FROM Recipe
                            INNER JOIN Origin ON Recipe.originId = Origin.id
                            INNER JOIN FoodType ON Recipe.foodTypeId = FoodType.id
                            INNER JOIN User ON Recipe.userId = User.id
                        Where Recipe.title LIKE %s
                        OR Recipe.description LIKE %s
                        OR Recipe.instructions LIKE %s
                        OR User.fName LIKE %s
                        OR User.lName LIKE %s
                        OR FoodType.type LIKE %s
                        OR Origin.name LIKE %s
                    """
                    cursor.execute(query, ("%"+ keyword+ "%", "%"+ keyword+ "%", "%"+ keyword+ "%", "%"+ keyword+ "%", "%"+ keyword+ "%", "%"+ keyword+ "%", "%"+ keyword+ "%",)) 
                    for(title, cookTime, servingSize, description, instructions, originName, type, fName, lName) in cursor:
                        print(f"Recipe Name: {title} Cook Time: {cookTime} Serving Size: {servingSize} Description: {description} Instructions: {instructions} Country of Origin: {originName}, Type: {type} User: {fName} {lName}")
                elif(command == "3"):
                    pass 
            elif(command == "2"):
                print("placeholder")
            elif(command == "3"):
                break
     
        elif command == "3":
            print("new user")
        elif command == "4":
            done = True
        else:
            print("Please enter a valid number.")

        
    

except mysql.connector.Error as err:
    print(err)
else:
    #Invoked if no exception was thrown
    cnx.close()
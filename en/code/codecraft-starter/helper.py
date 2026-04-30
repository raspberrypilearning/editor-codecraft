#############
# CodeCraft #
#############

# ---
# Game functions
# ---

# import the modules and variables needed
import turtle
import random
from math import ceil

# Import shared game state and settings from main.py
import main as game

TILESIZE = 20
# the number of inventory game.resources per row
INVWIDTH = 8
drawing = False

# moves the player left 1 tile.
def moveLeft():
    #global playerX
    if drawing == False and game.playerX > 0:
        oldX = game.playerX
        game.playerX -= 1
        drawResource(oldX, game.playerY)
        drawResource(game.playerX, game.playerY)


# moves the player right 1 tile.
def moveRight():
    #global playerX, game.MAPWIDTH
    if drawing == False and game.playerX < game.MAPWIDTH - 1:
        oldX = game.playerX
        game.playerX += 1
        drawResource(oldX, game.playerY)
        drawResource(game.playerX, game.playerY)


# moves the player up 1 tile.
def moveUp():
    #global playerY
    if drawing == False and game.playerY > 0:
        oldY = game.playerY
        game.playerY -= 1
        drawResource(game.playerX, oldY)
        drawResource(game.playerX, game.playerY)


# moves the player down 1 tile.
def moveDown():
    #global playerY, game.MAPHEIGHT
    if drawing == False and game.playerY < game.MAPHEIGHT - 1:
        oldY = game.playerY
        game.playerY += 1
        drawResource(game.playerX, oldY)
        drawResource(game.playerX, game.playerY)


# picks up the resource at the player's position.
def pickUp():
   # global playerX, playerY
    drawing = True
    currentTile = world[game.playerX][game.playerY]
    # if the user doesn't already have too many...
    if game.inventory[currentTile] < game.MAXTILES:
        # player now has 1 more of this resource
        game.inventory[currentTile] += 1
        # the player is now standing on dirt
        world[game.playerX][game.playerY] = game.DIRT
        # draw the new DIRT tile
        drawResource(game.playerX, game.playerY)
        # redraw the inventory with the extra resource.
        drawInventory()
        # drawPlayer()


# place a resource at the player's current position
def place(resource):
    print("placing: ", game.names[resource])
    # only place if the player has some left...
    if game.inventory[resource] > 0:
        # find out the resourcee at the player's current position
        currentTile = world[game.playerX][game.playerY]
        # pick up the resource the player's standing on
        # (if it's not DIRT)
        if currentTile is not DIRT:
            game.inventory[currentTile] += 1
        # place the resource at the player's current position
        world[game.playerX][game.playerY] = resource
        # add the new resource to the inventory
        game.inventory[resource] -= 1
        # update the display (world and inventory)
        drawResource(game.playerX, game.playerY)
        drawInventory()
        # drawPlayer()
        print("   Placing", game.names[resource], "complete")
    # ...and if they have none left...
    else:
        print("   You have no", game.names[resource], "left")


# craft a new resource
def craft(resource):
    print("Crafting: ", game.names[resource])
    # if the resource can be crafted...
    if resource in game.crafting:
        # keeps track of whether we have the game.resources
        # to craft this item
        canBeMade = True
        # for each item needed to craft the resource
        for i in game.crafting[resource]:
            # ...if we don't have enough...
            if game.crafting[resource][i] > game.inventory[i]:
                # ...we can't craft it!
                canBeMade = False
                break
        # if we can craft it (we have all needed game.resources)
        if canBeMade == True:
            # take each item from the inventory
            for i in game.crafting[resource]:
                game.inventory[i] -= game.crafting[resource][i]
            # add the crafted item to the inventory
            game.inventory[resource] += 1
            print("   Crafting", game.names[resource], "complete")
        # ...otherwise the resource can't be crafted...
        else:
            print("   Can't craft", game.names[resource])
        # update the displayed inventory
        drawInventory()


# creates a function for placing each resource
def makeplace(resource):
    return lambda: place(resource)


# attaches a 'placing' function to each key press
def bindPlacingKeys():
    for k in game.placekeys:
        screen.onkey(makeplace(k), game.placekeys[k])


# creates a function for crafting each resource
def makecraft(resource):
    return lambda: craft(resource)


# attaches a 'crafting' function to each key press
def bindCraftingKeys():
    for k in game.craftkeys:
        screen.onkey(makecraft(k), game.craftkeys[k])


# draws a resource at the position (y,x)
def drawResource(y, x):
    # this variable stops other stuff being drawn
    global drawing
    # only draw if nothing else is being drawn
    if drawing == False:
        # something is now being drawn
        drawing = True
        # draw the resource at that position in the tilemap, using the correct image
        rendererT.goto((y * TILESIZE) + 20, height - (x * TILESIZE) - 20)
        # draw tile with correct texture
        texture = game.textures[world[y][x]]
        rendererT.shape(texture)
        rendererT.stamp()
        if game.playerX == y and game.playerY == x:
            rendererT.shape(game.playerImg)
            rendererT.stamp()
        screen.update()
        # nothing is now being drawn
        drawing = False


# draws the world map
def drawWorld():
    # loop through each row
    for row in range(game.MAPHEIGHT):
        # loop through each column in the row
        for column in range(game.MAPWIDTH):
            # draw the tile at the current position
            drawResource(column, row)


# draws the inventory to the screen
def drawInventory():
    # this variable stops other stuff being drawn
    global drawing
    # only draw if nothing else is being drawn
    if drawing == False:
        # something is now being drawn
        drawing = True
        # use a rectangle to cover the current inventory
        rendererT.color(game.BACKGROUNDCOLOUR)
        rendererT.goto(0, 0)
        rendererT.begin_fill()
        # rendererT.setheading(0)
        for i in range(2):
            rendererT.forward(inventory_height - 60)
            rendererT.right(90)
            rendererT.forward(width)
            rendererT.right(90)
        rendererT.end_fill()
        rendererT.color("black")
        # display the 'place' and 'craft' text
        for i in range(1, num_rows + 1):
            rendererT.goto(20, (height - (game.MAPHEIGHT * TILESIZE)) - 20 - (i * 100))
            rendererT.write("place")
            rendererT.goto(20, (height - (game.MAPHEIGHT * TILESIZE)) - 40 - (i * 100))
            rendererT.write("craft")
        # set the inventory position
        xPosition = 70
        yPostition = height - (game.MAPHEIGHT * TILESIZE) - 60
        itemNum = 0
        for i, item in enumerate(game.resources):
            # add the image
            rendererT.goto(xPosition + 10, yPostition)
            rendererT.shape(game.textures[item])
            rendererT.stamp()
            # add the number in the inventory
            rendererT.goto(xPosition, yPostition - TILESIZE)
            rendererT.write(game.inventory[item])
            # add the name
            rendererT.goto(xPosition, yPostition - TILESIZE - 20)
            rendererT.write("[" + game.names[item] + "]")
            # add key to place
            rendererT.goto(xPosition, yPostition - TILESIZE - 40)
            rendererT.write(game.placekeys[item])
            # add key to craft
            if game.crafting.get(item) != None:
                rendererT.goto(xPosition, yPostition - TILESIZE - 60)
                rendererT.write(game.craftkeys[item])
            # move along to place the next inventory item
            xPosition += 50
            itemNum += 1
            # drop down to the next row every 10 items
            if itemNum % INVWIDTH == 0:
                xPosition = 70
                itemNum = 0
                yPostition -= TILESIZE + 80
        drawing = False


# generate the instructions, including crafting rules
def generateInstructions():
    game.instructions.append("Crafting rules:")
    # for each resource that can be crafted...
    for rule in game.crafting:
        # create the crafting rule text
        craftrule = game.names[rule] + " = "
        for resource, number in game.crafting[rule].items():
            craftrule += str(number) + " " + game.names[resource] + " "
        # add the crafting rule to the instructions
        game.instructions.append(craftrule)
    # display the instructions
    yPos = height - 20
    for item in game.instructions:
        rendererT.goto(game.MAPWIDTH * TILESIZE + 40, yPos)
        rendererT.write(item)
        yPos -= 20


# generate a random world
def generateRandomWorld():
    # loop through each row
    for row in range(game.MAPHEIGHT):
        # loop through each column in that row
        for column in range(game.MAPWIDTH):
            # pick a random number between 0 and 10
            randomNumber = random.randint(0, 10)
            # WATER if the random number is a 1 or a 2
            if randomNumber in [1, 2]:
                tile = game.WATER
            # GRASS if the random number is a 3 or a 4
            elif randomNumber in [3, 4]:
                tile = game.GRASS
            # otherwise it's DIRT
            else:
                tile = game.DIRT
            # set the position in the tilemap to the randomly chosen tile
            world[column][row] = tile


# ---
# Set up the game and start the main loop
# ---

def run():
    # Make these available to other functions
    global screen, rendererT, world, width, height, inventory_height, num_rows, drawing

    # create a new 'screen' object
    screen = turtle.Screen()
    # calculate the width and height
    width = (TILESIZE * game.MAPWIDTH) + max(200, INVWIDTH * 50)
    num_rows = int(ceil((len(game.resources) / INVWIDTH)))
    inventory_height = num_rows * 120 + 40
    height = (TILESIZE * game.MAPHEIGHT) + inventory_height

    screen.setup(width, height)
    screen.setworldcoordinates(0, 0, width, height)
    screen.bgcolor(game.BACKGROUNDCOLOUR)
    screen.listen()

    # register the player image
    screen.register_shape(game.playerImg)
    # register each of the resource images
    for texture in game.textures.values():
        screen.register_shape(texture)

    # create another turtle to do the graphics drawing
    rendererT = turtle.Turtle()
    rendererT.hideturtle()
    rendererT.penup()
    rendererT.speed(0)
    rendererT.setheading(90)

    # create a world of random game.resources.
    world = [[game.DIRT for w in range(game.MAPHEIGHT)] for h in range(game.MAPWIDTH)]

    # map the keys for moving and picking up to the correct functions.
    screen.onkey(moveUp, "w")
    screen.onkey(moveDown, "s")
    screen.onkey(moveLeft, "a")
    screen.onkey(moveRight, "d")
    screen.onkey(pickUp, "space")

    # set up the keys for placing and crafting each resource
    bindPlacingKeys()
    bindCraftingKeys()
 
    # these functions are definƒed above
    generateRandomWorld()
    drawWorld()
    drawInventory()
    generateInstructions()
    
    # keep window open
    screen.mainloop()

# Run the game if you press Run on this file
if __name__ == "__main__":
    run()

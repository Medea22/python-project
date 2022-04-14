from sys import exit

boxes = {
    "name": "boxes",
    "type": "furniture",
}

cargo = {
    "name": "cargo",
    "type": "furniture",
}

door_c = {
    "name": "door c",
    "type": "door",
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

cargo_room = {
    "name": "cargo room",
    "type": "room",
}

outside = {
  "name": "outside",
}


main_hall = {
    "name": "main hall",
    "type": "room",
}

trash_room = {
    "name": "trash room",
    "type": "room",
}

rubbish = {
    "name": "rubbish",
    "type": "furniture",
}

door_t = {
    "name" : "door t",
    "type" : "door",
}

key_t = {
    "name": "key for door t",
    "type": "key",
    "target": door_t,
}

door_d = {
    "name" : "door d",
    "type" : "door",
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

door_b = {
    "name" : "door b",
    "type" : "door",
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

door_m = {
    "name" : "door m",
    "type" : "door",
}

key_m = {
    "name": "key for door m",
    "type": "key",
    "target": door_m,
}

control_panel = {
    "name" : "control panel",
    "type" : "door",
}

megabatteries = {
    "name": "megabatteries",
    "type": "key",
    "target": control_panel,
}


dorms = {
    "name" : "dorms",
    "type" : "room",
}

single_bed = {
    "name" : "single bed",
    "type" : "furniture",
}

double_bed = {
    "name" : "double bed",
    "type" : "furniture",
}

bathroom = {
    "name" : "bathroom",
    "type" : "room",
}

toilet = {
    "name" : "toilet",
    "type" : "furniture",
}

bathtub = {
    "name" : "bathtub",
    "type" : "furniture",
}

cockpit = {
    "name" : "cockpit",
    "type" : "room",
}

all_rooms = [outside, cargo_room, bathroom, dorms, trash_room, main_hall, cockpit]

all_doors = [door_c, door_d, door_b, door_t, door_m, control_panel]

# define which items/rooms are related

object_relations = {
    "cargo room": [boxes, cargo, door_c],
    "boxes": [key_c],
    "cargo": [key_d],
    "outside": [control_panel],
    "door c": [cargo_room, main_hall],
    "main hall":[door_c, door_d, door_t, door_b, door_m],
    "trash room":[rubbish, door_t],
    "door t":[trash_room, main_hall],
    "door b":[bathroom, main_hall],
    "bathroom":[toilet, bathtub, door_b],
    "toilet":[megabatteries],
    "bathtub":[key_m],
    "dorms":[single_bed, double_bed, door_d],
    "single bed":[key_b],
    "double bed":[key_t],
    "door d":[dorms, main_hall],
    "cockpit":[door_m, control_panel],
    "door m":[cockpit, main_hall],
    "control panel":[cockpit, outside],
    
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": cargo_room,
    "keys_collected": [],
    "target_room": outside
}

def linebreak():
    """
    Print a line break
    """
    print("\n")

def start_game():
    """
    Start the game
    """
    print("----------------------------------------------------------------------\n----------------------------------------------------------------------\nATTENTION!! ATTENTION!! CAPTAIN TO ALL CREW. THE MEGABATTERIES THAT MAKE THE SPACESHIP\nWORK HAVE DISSAPEARED AND WITHOUT THEM WE CANNOT MAKE THE SPACESHIP WORK.\nTHE OXYGEN IS RUNNING OUT AND IF WE DON'T FIND THE MEGABATTERIES SOON WE WILL ALL PASS OUT!\nPLEASE FIND THE MEGABATTERIES AND BRING THEM SAFELY TO THE COCKPIT, GOOD LUCK COMRADES!!\n----------------------------------------------------------------------\n----------------------------------------------------------------------")
    linebreak()
    play_room(game_state["current_room"])
    
def start_again():
    game_state["current_room"] = cargo_room
    game_state["keys_collected"] = []
    object_relations["boxes"] = [key_c]
    object_relations["cargo"] = [key_d]
    object_relations["single bed"] = [key_b]
    object_relations["double bed"] = [key_t]
    object_relations["toilet"] = [megabatteries]
    object_relations["bathtub"] = [key_m]
    #return game_state, start_game()
    start_game()

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("THANK YOU COMRADE! You saved the life of all the crew, myself included! You will be properly rewarded as soon as we get to the Earth!!")
        exit(0)
    else:
        explore_room(room)
        examine_item(input("What would you like to examine?\n\n").strip())
    



def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You are now in the " + room["name"] + ". You can find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have.\n----------------------------------------------------------------------"
                    next_room = get_next_room_of_door(item, current_room)
                    linebreak()
                else:
                    output += "It is locked but you don't have the key.\n----------------------------------------------------------------------"
                    linebreak()
                    
            elif (item["name"] == "rubbish"):
                print("\n----------------------------------------------------------------------\nOh, no! A misterious creature appeared, RUN, RUUUUUN!!\n\n...\n\nToo late...\n\n")
                start_again()
                      
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find a " + item_found["name"] + "!!\n----------------------------------------------------------------------"
                    linebreak()
                else:
                    output += "There isn't anything interesting about it.\n----------------------------------------------------------------------"
                    linebreak()
            print(output)
            break

    if(output is None):
        print("Oh, you think you are funny? We don't have time to loose! You will be punished for this interruption.")
        start_again()
            
        #print("The item you requested is not found in the current room.\n----------------------------------------------------------------------")
    
    if(next_room and input("\nDo you want to go to the next room? Enter 'yes' or 'no'\n----------------------------------------------------------------------\n").strip() == 'yes'):
        print("----------------------------------------------------------------------\n")
        play_room(next_room)
    else:
        linebreak()
        examine_item(input("What would you like to examine?\n\n").strip()) #<-- por que si pongo esto no funciona??
        


    
    
game_state = INIT_GAME_STATE.copy()  # Variable that saves the GAME STATE, it's a dictionary.


start_game()     
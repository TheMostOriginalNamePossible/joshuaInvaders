My main goal in this project was to make something functional and potentially expandable.
I may expand this more in the future for entertainment purposes.
I wanted to add quite a bit, but I also knew I could only add so much,
so I favored functionality over fun. Despite this,
the sounds that I added make it surprisingly entertaining despite the only two things you're doing
is shooting and dodging bullets. The music is a big inside joke among me and my collaborator.

I was originally going to have my collaborator contribute some code, so I could make the game bigger in
the time period given. I am terrible with documenting and communicating my code, so
I decided against doing that. Plus, I didn't even ask if I could for the project. I decided to just ask
him to make me silly images for the game instead. He is added to project as a collaborator and be referenced as such
for his image contributions.

For the player, I will add controls since most of the instructions are in the game itself.
If for some reason you have a monitor smaller the 1080x720, you can change SCREEN_WIDTH and SCREEN_HEIGHT in
joshuaInvadersMain.py
P - pauses the game
Left Mouse Button - shoots lasers, it is also used to click menu options
The player character follows the mouse.

I had to use 2 different files for the game because it would be a pain to scroll through that many objects to
debug code. I would also like to note that forgetting to reset a boolean variable to false in the code
caused my mouse to stay hovering over a start over button and I had to yank it out of the window. I used a mix
of simpleGE.py, some stuff I found on the pygame website. I ended up deciding to use multiple groups and straying
away from the previous game's mechanisms. I didn't like the idea of it closing the instructions
window to open the game. I decided to define a bunch of boolean variables to have specific menu states.
I also used nested while loop to create a functional pause menu. There might be another of doing it without
a nested while loop, but it works, and changing that is more hassle than it's worth.

Since my game document was very vague (and intentionally so), it didn't really stray too far off from it.
When I wrote it out, I had a specific game in mind, Chicken Invaders 4. Look it up if you don't know what it is.
That's what I was going for gameplay wise over the traditional space invaders type game.

A choking point when I was using simpleGE.py. I ran into an annoying visual bug when using groups. Since I was
set on using groups, I had to change the whole __mainLoop because the for loop at the end caused the visual bug.
There's probably

I stayed on track by coding the general structure of classes and methods I would need using the previous game
as a reference point. I also wrote a plans document to get some overarching goals, very close goals, bugs that
needed fixed that I got stuck on, and stuff I already did. This is

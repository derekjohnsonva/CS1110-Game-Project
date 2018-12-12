# Derek Johnson dej3tc
# sprites found from OpenGameArt.org
11 / 18 / 2018
import pygame
import gamebox
import random
'''
We will be attempting to create a game with similar mechanics to the classic
arcade games missile command and phoenix.  There will be a defense ship
that is trying to counter the attack of incoming rockets being fired from enemy ships.
These enemy ships are tyring to fly past the defense ship and suicide bomb earth.
We are also going to try to incorporate a boss battle into the end of the game.

"The Optional Features that we are going to implement are:
Animation: We are going to have a sprite sheet that will allow us to animate both 
the defending and the attacking ships.  There should be a missile firing animation but 
the actual missile will not be a sprite.  This will be accomplished using two sprite sheets.
One for the attacking and one for the defending ship.
Enemies:  These will be rival ships trying to attack earth.  They will fly and perform 
evasive maneuvers to try to escape fire from the defense ship.  The ships will all fly in a 
similar pattern to the way ships fly in phoenix, looping and swerving to avoid being destroyed by the
defending ship
Health Meter:  This will keep a running total of the earth's health.  As enemy ships fly past the 
defending ship, the health will go down.  When it hits zero the game is reset.  This will be displayed in 
the corner of the screen
Collectibles:  There will be power ups that can be collected as enemies are destroyed.  These power ups
will make missiles travel faster and can help regain earth's health.
'''

width = 800
height = 600
camera = gamebox.Camera(width,height)
game_started = False
instructions = '''
    You are the last space ship of the US batallion,
    who must destroy the invading enemy space ships 
    as they descend upon Earth.  Use the [SPACE] bar to fire your gun 
    at them and use the [ARROW] keys to move around space.

    Press any key to begin.
'''


def draw_title(keys):
    '''
    Draws all components of the title screen
    '''
    global game_started
    global instructions

    if keys:  # Start the game if any key at all pressed
        game_started = True
    keys.clear()  # So that key is not logged in the next tick

    to_draw = []  # This list will contain all boxes we draw this tick

    # Make the Game Title text
    title_box = gamebox.from_text(camera.x, camera.y, 'SPACE FORCE', 80, 'blue', True)
    to_draw.append(title_box)
    ypos = camera.y + 120
    for line in instructions.split('\n'):
        to_draw.append(gamebox.from_text(camera.x, ypos, line, 29, 'red'))
        ypos += 20
    top_left_enemy = gamebox.from_image(60, 70, 'enemy_1.jpg')
    to_draw.append(top_left_enemy)
    top_right_enemy = gamebox.from_image(740, 70, 'enemy_2.jpg')
    to_draw.append(top_right_enemy)
    bottom_right_enemy = gamebox.from_image(740, 540, 'enemy_1.jpg')
    to_draw.append(bottom_right_enemy)
    bottom_left_enemy = gamebox.from_image(60, 540, 'enemy_2.jpg')
    to_draw.append(bottom_left_enemy)
    title_top_right_ship = gamebox.from_image(camera.x+220,camera.y-80,'ship_turned_1.jpg')
    to_draw.append(title_top_right_ship)
    title_top_left_ship = gamebox.from_image(camera.x-220,camera.y-80,'ship_turned_2.jpg')
    to_draw.append(title_top_left_ship)
    title_bottom_right_ship = gamebox.from_image(camera.x+220,camera.y+80,'ship_turned_4.jpg')
    to_draw.append(title_bottom_right_ship)
    title_bottom_left_ship = gamebox.from_image(camera.x-220,camera.y+80,'ship_turned_3.jpg')
    title_bottom_left_ship.rotate(15)
    to_draw.append(title_bottom_left_ship)
    for box in to_draw:
        camera.draw(box)
"""GAME"""

shipnum = 0
ship = gamebox.from_image(400,550,'goodship.jpg')
enemySheet = gamebox.load_sprite_sheet("astrominer.png", 3, 7)
explosion = gamebox.load_sprite_sheet('spritesheet.png',1,20)
space_background = gamebox.from_image(300,300,'space.jpg')
enemies = []
shipData = [1,1,1,1,2,3,3]  # number of lives each ship has
enemyData = []
bullets = []
collectibles = []
explosions = []
#counters and constants
counter = 0
bulletSpeed = 10     #how fast the bullets move
bulletTimer = 30
bulletTimerSpeed = 1  #how fast the bullets regenerate
enemySpeed = 1
enemyRegeneration = 50
lives = 10
powerups = 0
shipSpeed = 5
game_over = 0
enemy_counter = 0
def tick(keys):
    global counter, bulletSpeed, bulletTimer, bulletTimerSpeed, enemySpeed, enemyRegeneration, lives, powerups, shipSpeed, game_over, enemy_counter
    if game_started is False:
        draw_title(keys)
    else:
        counter += 1
        camera.draw(space_background)

        if ship.x > width:
            ship.x = 0
        if ship.x < 0:
            ship.x = width
        if ship.y <= 0:
            ship.y = 0
        if ship.y >= 600:
            ship.y = 600

        if pygame.K_RIGHT in keys:
            ship.x += shipSpeed
        if pygame.K_LEFT in keys:
            ship.x -= shipSpeed
        if pygame.K_UP in keys:
            ship.y -= shipSpeed
        if pygame.K_DOWN in keys:
            ship.y += shipSpeed

        if counter % enemyRegeneration == 0:
            shipnum = random.randint(0,6)
            xLocal = random.randint(50,750)
            newEnemy = gamebox.from_image(xLocal, -50, enemySheet[shipnum])
            enemies.append(newEnemy)
            enemyData.append(shipData[shipnum])

        for enemy in enemies:    #moving the enemy ships
            enemy.y += enemySpeed
            camera.draw(enemy)

        bulletTimer += bulletTimerSpeed
        if pygame.K_SPACE in keys and bulletTimer >= 30:       # firing bullets
            bullet = gamebox.from_color(ship.x, ship.y, 'yellow', 5, 20)
            bullets.append(bullet)
            bullets[-1].speedy = -(bulletSpeed)
            keys.remove(pygame.K_SPACE)

            bulletTimer = 0
        enemies_to_deelete = []
        for bullet in bullets:    #hitting targets with bullets
            enemies_to_deelete = []
            for x in range(0, len(enemies)):
                if bullet.touches(enemies[x]):
                    new_bang = gamebox.from_image(enemies[x].x, enemies[x].y, explosion[1])
                    camera.draw(new_bang)
                    enemyData[x] = enemyData[x]-1
                    bullets.remove(bullet)
                    if enemyData[x] <= 0:
                        explosions.append([gamebox.from_image(enemies[x].x,enemies[x].y,explosion[1]),0]) #adds explosion to list
                        enemies_to_deelete.append(enemies[x])
            bullet.move_speed()
            camera.draw(bullet)
        for explode in explosions:
            camera.draw(explode[0])
            explode[1] += 1
            if explode[1] >= 15:
                explosions.remove(explode)
            explode[0] = gamebox.from_image(explode[0].x, explode[0].y, explosion[explode[1]])
        for enemy in enemies_to_deelete:
            enemies.remove(enemy)
            enemy_counter += 1
        if counter % 300 == 0  and shipSpeed<20 and bulletTimerSpeed < 35:   #making new collectibles
            randx = random.randrange(30, 760)
            randy = random.randrange(20,300)
            newCollectible = gamebox.from_color(randx, randy, 'green', 30, 20)
            collectibles.append(newCollectible)

        for coin in collectibles:
            camera.draw(coin)

        for bullet in bullets:  #bullet collectible collision
            for coin in collectibles:
                if bullet.touches(coin):
                    bullets.remove(bullet)
                    collectibles.remove(coin)
                    bulletTimerSpeed += 2    #makes the ship shoot faster
                    powerups += 1
                    shipSpeed += 1

        camera.draw(ship)

        for enemy in enemies: #Gets rid of enemies if the ship runs into them
            if ship.touches(enemy):
                new_bang = gamebox.from_image(ship.x, ship.y, explosion[1])
                camera.draw(new_bang)
                enemies.remove(enemy)
                lives -=1

        for coin in collectibles:
            if ship.touches(coin):
                collectibles.remove(coin)
                bulletTimerSpeed += 2  # makes the ship shoot faster
                powerups += 1
                shipSpeed += 1

        for enemy in enemies:
            if enemy.y>640:
                enemies.remove(enemy)
                lives -= 1
        current_lives = gamebox.from_text(80, 50, 'Lives:' + str(lives), 50, 'white')
        kill_counter = gamebox.from_text(300, 50, 'Kills:'+str(enemy_counter),50,'white')
        if counter % 1000 == 0:
            enemySpeed += 1
            enemyRegeneration -= 5
        if lives <= 0:  # game over
            enemySpeed = 0
            enemyRegeneration = 0
            game_over = True
        if game_over:
            camera.draw(gamebox.from_text(camera.x, camera.y, "GAME OVER!", 70, "red"))
            gamebox.pause()
        bulletSpeedDisplay = gamebox.from_text(650,50,'Blaster Fuel:'+str(powerups), 40, 'white')  #drawing the collectible display
        camera.draw(bulletSpeedDisplay)
        camera.draw(kill_counter)
        camera.draw(current_lives)
    camera.display()


ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)


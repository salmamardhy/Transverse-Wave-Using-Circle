import pygame, pygame.gfxdraw, pygame.constants, pygame.locals, sys, pyautogui, math, pygame.locals
from pygame import mixer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pygame.init()

# WARNA
yellow = (241,232,94)
tosca = (89,246,253)

# LAYAR TAMPILAN
size = 1500, 900
surface = pygame.Surface(size)
screen = pygame.display.set_mode(size)
surface.set_colorkey((0, 0, 0)) # transparent colorkey (warna hitam)
pygame.display.set_caption("Transverse Wave Using Circle")

# KECEPATAN FRAME UNTUK UPDATE
FPS = 100
clock = pygame.time.Clock()

# NILAI AWAL
pause = False
radius = 35
kenaikan_radius = 5
angle = 0
n = 0

# NILAI AWAL GELOMBANG
kecepatan_sudut = 0.005
kenaikan_sudut  = 0.0049
center          = 50, 485
wave            = []

# PENGATURAN VOLUME - Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers() # menyambungkan perangkat dengan program 
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None) # interaksi perangkat dengan program
volume = cast(interface, POINTER(IAudioEndpointVolume)) # mengatur volume
volume.SetMasterVolumeLevel(-65.0, None) # setting suara awal saat program dimulai (-65 sd -3)

# MUSIK
mixer.music.load("sound1.mp3")

# PANJANG GELOMBANG SAMPAI UJUNG
batas_gelombang = 403
garis_penghubung = center[0] + 300

while True:
    bg = pygame.image.load("bg.jpg").convert()
    screen.blit(bg, (0, 0))
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            volume.SetMasterVolumeLevel(-15.0, None)
            sys.exit()

        if pygame.key.get_pressed()[pygame.K_p]:
            mixer.music.play(-1) # looping
            n = 1

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pause = True
            pygame.mixer.music.pause()

        if pygame.key.get_pressed()[pygame.K_UP]:
            radius += kenaikan_radius
            if radius > 70:
                radius = 70

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            radius -= kenaikan_radius
            if radius < 35:
                radius = 35

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            kecepatan_sudut += kenaikan_sudut
            if kecepatan_sudut > 0.25:
                kecepatan_sudut = 0.25
            pyautogui.press("volumeup", +1) 

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            kecepatan_sudut -= kenaikan_sudut
            if kecepatan_sudut < 0.005:
                kecepatan_sudut = 0.005
            pyautogui.press("volumedown", +1)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                volume.SetMasterVolumeLevel(-15.0, None)
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                pause = False
                pygame.mixer.music.unpause()

    font = pygame.font.Font('Digital-7.ttf', 38)
    tekskecepatan_sudut = font.render(f"{round(kecepatan_sudut, 10)}", True, tosca)
    amplitudo = font.render(f"{round(radius,10)}", True, tosca)

    surface.fill((0,0,0))
    surface.blit(tekskecepatan_sudut, (753, 703))
    surface.blit(amplitudo, (1045, 703))

    x, y = center
    for i in range(1, 2*n + 1, 2): # (start, stop, step)
        prevx, prevy = x, y
        x = x + (radius / i) * math.cos(angle * i) 
        y = y + (radius / i) * math.sin(angle * i)
        
        # LINGKARAN - aacircle(surface, x, y, r, color)
        pygame.gfxdraw.aacircle(surface, (prevx+600), (prevy), radius, yellow)
        pygame.gfxdraw.aacircle(surface, (prevx+600), (prevy), (radius)+1, yellow)

        # GARIS DALAM LINGKARAN - aaline(surface, color, start_pos, end_pos)
        pygame.draw.aaline(surface, yellow, (prevx+600, prevy), (x+600, y))
        pygame.draw.aaline(surface, yellow, (prevx+601, prevy), (x+601, y))

    angle += kecepatan_sudut
    wave.insert(0, y)

    # GARIS PENUNJUK/PENGHUBUNG - aaline(surface, color, start_pos, end_pos)
    pygame.draw.aaline(surface, tosca, (x+600, y), (garis_penghubung+420, wave[0]))

    # BULATAN PADA GARIS LINGKARAN - circle(surface, color, center, radius)
    pygame.draw.circle(surface, yellow, [x+600, y], 5)

    if len(wave) > batas_gelombang: 
        wave.pop()

    # POSISI AKHIR
    titik_wave = [(garis_penghubung + j + 420, w) for j, w in enumerate(wave)] # x, y
    if len(titik_wave) > 1:
        pygame.draw.aalines(surface, tosca , False, titik_wave)
        pygame.draw.aalines(surface, tosca , False, [(garis_penghubung + j + 420, w + 1.2) for j, w in enumerate(wave)])
        pygame.draw.aalines(surface, tosca , False, [(garis_penghubung + j + 420, w + 1.8) for j, w in enumerate(wave)])
import cv2
import time
import random
import elIzlemeModulu as htm
import pygame

#py game eklendi
pygame.init()

#oyun penceresi
GENISLIK,YUKSEKLIK= 713,475
pencere = pygame.display.set_mode((GENISLIK,YUKSEKLIK))
pygame.display.set_caption("Counter-Attack")

# Arka plan resmi
background = pygame.image.load("game module\images\caBG.png")
background = pygame.transform.scale(background, (GENISLIK,YUKSEKLIK))

#Ses
saldiri_sesi=pygame.mixer.Sound("game module\music\\attackSound.wav")
saldiri_sesi.set_volume(0.15)
savunma_sesi=pygame.mixer.Sound("game module\music\defendSound.wav")
savunma_sesi.set_volume(0.3)

pygame.mixer.music.load("game module\music\\backSound.wav")
pygame.mixer.music.set_volume(0.1)
pygame.time.delay(2500)
pygame.mixer.music.play(-1)

#Karakter resimleri
sovalye= pygame.image.load("game module\images\knight.png")
sovalye_koordinat = sovalye.get_rect()
sovalye_koordinat.topleft=(30,335) 

dusman= pygame.image.load("game module\images\dusman.png")
dusman_koordinat=dusman.get_rect()
dusman_koordinat.topleft=(500,253)

#yazılar
font_ismi = pygame.font.SysFont("impact",50,False,True) # font adı ve boyutu
font_ismi2 = pygame.font.SysFont("impact",30,False,True) # font adı ve boyutu

#VS Yazisi
yazi = font_ismi.render("VS",True,(0,0,255)) #1- Yazı, 2- Bozuklukları düzelt,3- Renk
yazi_koordinat = yazi.get_rect()#koordinat metodu
yazi_koordinat.topleft=(315,20)#koordinat

#Round Yazisi
round_sayisi = 1
round_yazisi = font_ismi2.render(f"ROUND {round_sayisi}",True,(0,0,0))
round_koordinati = round_yazisi.get_rect()
round_koordinati.topleft=(285,75)

kratos = font_ismi2.render("KRATOS",True,(255,0,0))
kratos_koordinat = kratos.get_rect()
kratos_koordinat.topleft=(100,15)

cronos = font_ismi2.render("CRONOS",True,(255,0,0))
cronos_koordinat = cronos.get_rect()
cronos_koordinat.topleft=(475,15)

kratos_can_degeri = 100
kratos_can_yazi = font_ismi2.render(f"{kratos_can_degeri}",True,(255,0,0))
kratos_can_yazi_koordinat = kratos.get_rect()
kratos_can_yazi_koordinat.topleft=(125,50)

chronos_can_degeri = 100
chronos_can_yazi = font_ismi2.render(f"{chronos_can_degeri}",True,(255,0,0))
chronos_can_yazi_koordinat = kratos.get_rect()
chronos_can_yazi_koordinat.topleft=(510,50)

#Can barı uzunluk
kratos_can_bari =200
cronos_can_bari =200
chronos_can_tersyon = 0

class Oyuncu:
    def __init__(self):
        self.health = 100
    
    def playerSecim(self, attackFingers=0):
        return attackFingers

class Bilgisayar:
    def __init__(self):
        self.health = 100

    def cpuSecim(self):
        return random.randint(1, 3)

player = Oyuncu()
computer = Bilgisayar()

def OyunAlgoritmasi(player_turn, parmakSayisi=0):
    global kratos_can_bari, cronos_can_bari,kratos_can_degeri,chronos_can_degeri,saldiri_sesi,savunma_sesi,chronos_can_tersyon,cronos_can_bari_ters_yon
    if player_turn:
        if parmakSayisi < 1 or parmakSayisi > 3:  # Parmağın 1 ile 3 arasında olup olmadığını kontrol et
            print("Parmağınızı 1, 2 veya 3 parmak olarak gösterin.\n")
            return True  # Oyun devam etmesi gerekiyor return player_turn diyebiliriz iki yer için
        else: 
            cpu_secim = computer.cpuSecim()
            oyuncu_secim = player.playerSecim(parmakSayisi)
            if  oyuncu_secim != cpu_secim:
                saldiri_sesi.play()
                chronos_can_degeri-=10
                computer.health -= 10
                cronos_can_bari -=20
                chronos_can_tersyon+=20
                
                print(f"OYUNCU\n-- Saldırı başarılı..Bilgisayar Kalan Can = {computer.health}\n")
            else:
                savunma_sesi.play()
                print("OYUNCU\n-- Saldırı başarısız\n")
    else:
        if parmakSayisi < 1 or parmakSayisi > 3:  # Parmağın 1 ile 3 arasında olup olmadığını kontrol et
            print("Parmağınızı 1, 2 veya 3 parmak olarak gösterin.\n")
            return True  # Oyun devam etmesi gerekiyor
        else:    
            cpu_secim = computer.cpuSecim()
            oyuncu_secim = player.playerSecim(parmakSayisi)
            if cpu_secim != oyuncu_secim:
                saldiri_sesi.play()
                kratos_can_degeri -= 10
                player.health -= 10
                kratos_can_bari -= 20
                
                print(f"BİLGİSAYAR\n-- Saldırı başarılı.Oyuncu Kalan Can = {player.health}\n")
            else:
                savunma_sesi.play()
                print("BİLGİSAYAR\n-- Saldırı Başarısız\n")
    
    if player.health <= 0:
        print("Bilgisayar kazandı!")
        return False
    elif computer.health <= 0:
        print("Oyuncu kazandı!")
        return False

    return True


def main():
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = htm.handDetector(detectionCon=1)
    tipIds = [4, 8, 12, 16, 20]
    
    #Değişkenler
    durum = True
    player_turn = True
    last_check_time = time.time()
    global round_sayisi, kratos_can_degeri, chronos_can_degeri
    saldiriSayisi=1

    while durum:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False) 

        #Parmak tespiti
        if len(lmList) != 0:
            fingers = []
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            #Toplam parmak sayısı 
            totalFingers = fingers.count(1)
            
            #Kameraya parmak sayısı ve round yazma
            cv2.putText(img, f'Parmak Sayisi : {totalFingers}', (200, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(img, f"ROUND : {saldiriSayisi}", (240, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.70, (50, 75, 200), 2)               
        
            #Her 2.5 saniyede bir parmak sayısına göre işlem
            if time.time() - last_check_time > 2.5:
                if totalFingers >= 1 and totalFingers <= 3:  # Yalnızca geçerli parmak sayısı durumunda sıra değişimi yapacak
                    if not OyunAlgoritmasi(player_turn, totalFingers):
                        break
                    round_sayisi += 1
                    saldiriSayisi+=1
                    player_turn = not player_turn
                    last_check_time = time.time()
                else:
                    cv2.putText(img, "Lutfen 1 ile 3 arasi parmak gosteriniz.", (100, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.70, (255, 255, 0), 2)               

            cv2.putText(img, f"PLAYER HEALTH: {player.health}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
            cv2.putText(img, f"COMPUTER HEALTH: {computer.health}", (385, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        
        #Can değerleri ve ROUND Yazısı Güncellemeleri
        round_yazisi = font_ismi2.render(f"ROUND {round_sayisi}", True, (0, 0, 0))
        kratos_can_yazi = font_ismi2.render(f"{kratos_can_degeri}", True, (255,250,255))
        chronos_can_yazi = font_ismi2.render(f"{chronos_can_degeri}", True, (255,255,255))

        # oyunu kapatmak için  x tuşuna basılması durumu
        for etkinlik in pygame.event.get():
            if etkinlik.type == pygame.QUIT:
                durum = False
        
        # arkaplan resmi
        pencere.blit(background,(0,0))
        
        #Saldıran Taraf Yazısı
        if player_turn == True:
            pygame.draw.circle(pencere,(0,0,255),(150,105),15,0) 
            cv2.putText(img, f"Saldiriyor", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        else:
            pygame.draw.circle(pencere,(0,0,255),(520,105),15,0) 
            cv2.putText(img, f"Saldiriyor", (550, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
        
        #VS Yazısı
        pencere.blit(yazi,yazi_koordinat)
        
        #ROUND Yazısı
        pencere.blit(round_yazisi,round_koordinati)
        
        #Kratos ve Chronos Yazıları
        pencere.blit(kratos,kratos_koordinat)
        pencere.blit(cronos,cronos_koordinat)
       
        #Kahraman ve Dusman Görselleri
        pencere.blit(sovalye,sovalye_koordinat)
        pencere.blit(dusman,dusman_koordinat)


        #Kratos ve cronos kırmızı can barları
        pygame.draw.rect(pencere, (255,0,0), (50,60,200,20)) 
        pygame.draw.rect(pencere, (255,0,0), (435,60,200,20))

        #Kratos ve cronos yeşil can barları
        pygame.draw.rect(pencere, (0,255,0), (50,60,kratos_can_bari,20)) 
        pygame.draw.rect(pencere, (0,255,0), (435+chronos_can_tersyon,60,cronos_can_bari,20))
        
        #Kratos ve Cronos can Yazısı
        pencere.blit(kratos_can_yazi,kratos_can_yazi_koordinat)
        pencere.blit(chronos_can_yazi,chronos_can_yazi_koordinat)
        
        #Ekranı sürekli güncelle
        pygame.display.update()


main()
pygame.quit()
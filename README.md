# digitaliskalaka_techsalad

Az idei digitális kalákára csapatunk egy szemét menedzser alkalmazást szeretne létrehozni. Legfontosabbnak látjuk, hogy minden közösségünkbe tartozó személyt segítsünk és neveljünk arra, hogy szelektíven gyűjtsék a szemetet, hisz ez egyik alap pillére a környezettudatos és tiszta környezetű társadalomnak.

Mindezt egy okos kuka-dobozzal szeretnénk elősegíteni, amibe ha valaki behelyez egy szemetet, az kijelzi, hogy melyik szemét kategóriába tartozik az adott dolog.
Mindemellett egy telefon applikációt is létre szeretnénk hozni, ami ha épp nincs kéznél a doboz, képfelismerés segítségével ugyancsak megmondja, hogy hova kell helyezni az adott szemetet. 
Kis térképpel látnánk el ezt az aplikációt, hogy megtudhassuk, hol van a legközelebbi szelektív kuka. 
Létrehozható eventeket építenénk be az applikációba, amikbe városunk lakói becsatlakozhatnak, hogy bizonyos helyeket tudjanak megtisztítani. A városlakóktól az idejüket nem kérjük ingyen, kedvezményeket ajánlanánk nekik színházjegyekhez, parkoláshoz, stb.

Architektúra:
Egy külső szerver-számítógépen fut majd a webszerver, ami fogadja a feltöltendő képeket, itt fut a képfeldolgozó algoritmus is, majd visszatérít egy választ, esetenként kiegészítő üzenetekkel.

A doboz egy Jetson Nano microcomputeren fut, ami fizikailag is be van építve a dobozba. Erre azért van szükség, hogyha az internetkapcsolat megszűnne, akkor is működhessen a képfelismerés, illetve a Jetsonnak van egy 40 lábas PIN-csatlakozási lehetősége is, amivel vezérelhetünk különböző szenzorokat is.

A szenzorok és a képfelismerés eredményét súlyozva átlagoljuk, így döntjük el, hogy hova tartozik a szemét.

Kiegészítő jelleggel kiszámoljuk a sűrűség megközelítő értékét, így eldöntve, hogy az adott szemét összepréselendő-e?
Szeretnénk figyelni, hogy az újrahasznosítandó szemét szennyezett-e?

Keressük az újrahasznosítási jelet is.
Tanítási lehetőség! - képeket lehet küldeni a betanító datasetnek.

eLSZÍNEZŐDÉSEK  






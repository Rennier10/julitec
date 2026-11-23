"""Catálogo de demostración: los más vendidos/top por plataforma y los estrenos.
Precios base en COP (datos demostrativos). Editable o reemplazable por una API/BD externa.

Imágenes: CDN Steam library_600x900.jpg (portrait) donde existe.
Para juegos recientes sin esa imagen y los exclusivos Switch/PS5 sin PC se usan las
URLs completas con hash del header de Steam (verificadas 200 con la Steam API),
o IGDB para exclusivos sin Steam."""
PF = {"PC": .9, "PS5": 1, "XBOX": 1, "PS4": .8, "SWITCH": 1}
ALL = ["PC", "PS5", "PS4", "XBOX", "SWITCH"]
AK = "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps"
IG = "https://images.igdb.com/igdb/image/upload/t_cover_big"

# (id, título, categoría, plataformas, precio base, rating, %desc, ranking, lanzamiento, colores, estreno, imagen)
_R = [
 (1,  "Grand Theft Auto VI",           "Acción",        ["PS5","XBOX"],                     312289, 4.9, 19,  1,  "2026-11-19", ("#ff4fa0","#5b2bd6"), True,
      f"{IG}/co8tf0.jpg"),                                           # IGDB, verificado 200
 (2,  "EA SPORTS FC 27",               "Deportes",      ["PC","PS5","PS4","XBOX","SWITCH"], 289900, 4.5, 15,  2,  "2026-09-25", ("#6a2cff","#12d18e"), True,
      f"{AK}/4080220/ff6a3779f1ca83aae8ad3878454f6c11008ea24d/header.jpg?t=1793610006"),
 (3,  "Red Dead Redemption 2",         "Aventura",      ["PC","PS5","PS4","XBOX"],          129900, 4.9, 53,  3,  "2018-10-26", ("#d7261e","#3a0d0a"), False,
      f"{AK}/1174180/library_600x900.jpg"),
 (4,  "Grand Theft Auto V",            "Acción",        ["PC","PS5","PS4","XBOX"],           89900, 4.7, 40,  4,  "2013-09-17", ("#2fb37c","#10243a"), False,
      f"{AK}/271590/library_600x900.jpg"),
 (5,  "Minecraft Java & Bedrock",      "Aventura",      ["PC","PS5","PS4","XBOX","SWITCH"], 111000, 4.8, 48,  5,  "2011-11-18", ("#5da83a","#3b2a1a"), False,
      f"{AK}/2566040/header.jpg"),                                   # no tiene 600x900, header ok
 (6,  "Call of Duty: Modern Warfare 4","Shooter",       ["PC","PS5","XBOX"],                259900, 4.3, 43,  6,  "2026-10-23", ("#4a4f55","#0b0d10"), True,
      f"{AK}/4435490/0c492be3204835d71e8b454b6eb1817f8ff68c0d/header.jpg?t=1794873974"),
 (7,  "Elden Ring",                    "RPG de acción", ["PC","PS5","PS4","XBOX"],          179900, 4.8, 30,  7,  "2022-02-25", ("#d9a441","#1b1408"), False,
      f"{AK}/1245620/library_600x900.jpg"),
 (8,  "Phantom Blade Zero",            "Acción",        ["PC","PS5"],                       219900, 4.6, 26,  8,  "2026-09-09", ("#8a6a3b","#14100a"), True,
      f"{AK}/4115450/7f882f889630270d3d3fb93825ac6f55b55e7a6c/header.jpg?t=1793261976"),
 (9,  "The Witcher 3: Wild Hunt",      "RPG",           ["PC","PS5","PS4","XBOX","SWITCH"],  69900, 4.9, 70,  9,  "2015-05-19", ("#9b2226","#1d1d1d"), False,
      f"{AK}/292030/library_600x900.jpg"),
 (10, "Cyberpunk 2077",                "RPG",           ["PC","PS5","XBOX"],                149900, 4.6, 50,  10, "2020-12-10", ("#f5e90a","#16213e"), False,
      f"{AK}/1091500/library_600x900.jpg"),
 (11, "Hogwarts Legacy",               "Aventura",      ["PC","PS5","PS4","XBOX","SWITCH"], 159900, 4.5, 45,  11, "2023-02-10", ("#7a5cff","#1a1236"), False,
      f"{AK}/990080/library_600x900.jpg"),
 (12, "The Elder Scrolls V: Skyrim",   "RPG",           ["PC","PS5","XBOX","SWITCH"],        99900, 4.8, 79,  12, "2011-11-11", ("#9fb4c7","#0c1218"), False,
      f"{AK}/489830/library_600x900.jpg"),
 (13, "Forza Horizon 5",               "Carreras",      ["PC","XBOX"],                      139900, 4.7, 35,  13, "2021-11-09", ("#ff7a00","#0b3d91"), False,
      f"{AK}/1551360/library_600x900.jpg"),
 (14, "God of War Ragnarök",           "Acción",        ["PS5","PS4","PC"],                 199900, 4.9, 25,  14, "2022-11-09", ("#5aa9e6","#0e1a2b"), False,
      f"{AK}/2322010/library_600x900.jpg"),
 (15, "Baldur's Gate 3",               "RPG",           ["PC","PS5","XBOX"],                169900, 4.9, 15,  15, "2023-08-03", ("#b5179e","#240046"), False,
      f"{AK}/1086940/library_600x900.jpg"),
 (16, "Marvel's Spider-Man 2",         "Acción",        ["PS5","PC"],                       219900, 4.7, 30,  16, "2023-10-20", ("#e63946","#1d3557"), False,
      f"{AK}/2651280/library_600x900.jpg"),
 (17, "Zelda: Tears of the Kingdom",   "Aventura",      ["SWITCH"],                         249900, 4.9, 10,  17, "2023-05-12", ("#4cc9a6","#1b3a2b"), False,
      f"{IG}/co5vmg.jpg"),                                           # IGDB, verificado 200
 (18, "Mario Kart 8 Deluxe",           "Carreras",      ["SWITCH"],                         239900, 4.8, 10,  18, "2017-04-28", ("#e63946","#1e88e5"), False,
      f"{IG}/co6cl5.jpg"),                                           # IGDB, verificado 200
]
GAMES = []
for i, t, c, pl, p, r, d, rk, rel, col, new, img in _R:
    GAMES.append({"id": i, "title": t, "category": c, "platforms": pl, "rating": r, "discount": d,
                  "rank": rk, "release": rel, "colors": list(col), "new": new, "base_price": p,
                  "cover": f"/covers/{i}.jpg",   # portada local opcional (tiene prioridad si existe)
                  "image_url": img,              # portada remota CDN Steam / IGDB
                  "prices": {x: round(p * PF[x] * (100 - d) / 100) for x in pl},
                  "old_prices": {x: round(p * PF[x]) for x in pl}})

ASSET_FOLDER = "./assets"
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)

_tanks = (
    "churchill", "Crusader", "KV-1",
    "Lee", "M13", "matilda", "panther",
    "panzer", "sherman", "stuart", "T-26",
    "T-34", "Tiger"
)

_effects = (
    "Exhaust_Fire_up", "Exhaust_Fire_down", "Tire_Track_1", "Tire_Track_2",
    "Explosion1", "Explosion2", "Explosion3", "Explosion4", "Explosion5"
)

# assets
tank_assets = [f"/Tanks/{tank}.gif" for tank in _tanks]
effect_assets = [f"/Effects/{effect}.gif" for effect in _effects]

# OWAPI API Docs

## Changelog

    - 2017-08-03 - **Added new `rolling_averages` key. This contains averages over 10 minutes.**

## Notes

Regions and platforms can be overridden with URL parameters.

### Regions (V3)

In V3, all regions are automatically checked. Data is returned for any regions the user is in. The other regions return
`null`. See V3 results below.

### Platforms

You can override the platform with `?platform=<pc|xbl|psn>`. This defaults to `pc`.

### Formatting

The default output is standard JSON, but you can prettify it with `?format=json_pretty` to have it
in a more readable format. (The other option is installing a browser plugin, such as
[JSONView](https://jsonview.com/).

#### Field formatting

Field names inside the inner dict will correspond to all of the cards shown inside the
[PlayOverwatch](https://playoverwatch.com/en-us/career/pc/eu/Downy-2877) pages corresponding to
the users, with a slight formatting tweak:

 - All nonalphanumeric characters are removed
 - All spaces are replaced with underscores
 - The entire fields are lowercase

### Levels

The levels returned by the API are **not** the final levels. To calculate the final level,
use `(prestige * 100) + level`.

### Time fields

Unless otherwise specified, time fields are always in ***hours***.

---

## V3

### `GET /api/v3/u/:battletag/blob`
**Get a blob of information about user stats, achievements, and heroes.**

*Example:*

`https://owapi.net/api/v3/u/Dad-12262/blob`

*Result:*

```json
{

    "_request": {
        "api_ver": 3,
        "route": "/api/v3/u/Dad-12262/blob"
    },
    "kr": null,
    "eu": null,
    "us": {
        "stats": {},
        "heroes": {},
        "achievements": {}
    },
    "any": null

}
```

See below for detailed response on `stats`, `heroes`, and `achievements`.

### `GET /api/v3/u/:battletag/stats`
**Get user stats, both competitive & quickplay**

*Example:*

`https://owapi.net/api/v3/u/Dad-12262/stats`

*Result:*

A `stats` key containing several subkeys:

   - `competitive` - displaying your competitive statistics
   - `quickplay` - displaying your quickplay statistics

Each of these will have several other keys:

   - `overall_stats` - These are useful overall stats including winrate, level, prestige, game count, competitive rank,
   losses, wins, games.
   - `game_stats` - These show total statistics over all games.
   - `average_stats` - These are calculated by Blizzard as the average statistics.

```json
{

    "_request": {
        "api_ver": 3,
        "route": "/api/v3/u/Dad-12262/stats"
    },
    "kr": null,
    "eu": null,
    "us": {
        "stats": {
            "competitive": {
                "overall_stats": {
                    "win_rate": 52,
                    "level": 20,
                    "prestige": 1,
                    "avatar": "https://blzgdapipro-a.akamaihd.net/game/unlocks/0x0250000000000BBA.png",
                    "wins": 9,
                    "games": 17,
                    "comprank": 2395,
                    "losses": 8,
                    "endorsement_level": 2,
                    "endorsement_shotcaller": 0,
                    "endorsement_sportsmanship": 0,
                    "endorsement_teammate": 0,
                    "rank_image": "https://d1u1mce87gyfbn.cloudfront.net/game/playerlevelrewards/0x025000000000092A_Border.png",
                    "tier": null
                },
                "game_stats": {
                    "objective_kills": 121.0,
                    "games_won": 9.0,
                    "kpd": 1.92,
                    "objective_kills_most_in_game": 26.0,
                    "time_spent_on_fire_most_in_game": 0.075,
                    "healing_done": 15798.0,
                    "defensive_assists": 20.0,
                    "offensive_assists": 4.0,
                    "final_blows_most_in_game": 22.0,
                    "objective_time": 0.37027777777777776,
                    "melee_final_blows": 3.0,
                    "medals": 37.0,
                    "cards": 4.0,
                    "multikill_best": 4.0,
                    "overwatch.guid.0x086000000000042e": 8.0,
                    "multikills": 4.0,
                    "defensive_assists_most_in_game": 11.0,
                    "offensive_assists_most_in_game": 2.0,
                    "melee_final_blow_most_in_game": 1.0,
                    "damage_done": 201576.0,
                    "medals_silver": 12.0,
                    "medals_gold": 12.0,
                    "healing_done_most_in_game": 2597.0,
                    "environmental_kills": 5.0,
                    "medals_bronze": 13.0,
                    "solo_kills": 29.0,
                    "time_spent_on_fire": 0.33999999999999997,
                    "eliminations_most_in_game": 44.0,
                    "final_blows": 152.0,
                    "time_played": 3.0,
                    "environmental_deaths": 6.0,
                    "solo_kills_most_in_game": 22.0,
                    "damage_done_most_in_game": 22230.0,
                    "games_played": 17.0,
                    "eliminations": 315.0,
                    "objective_time_most_in_game": 0.060000000000000005,
                    "deaths": 164.0
                },
                "competitive": true,
                "average_stats": {
                    "healing_done_avg": 929.0,
                    "eliminations_avg": 18.52,
                    "melee_final_blows_avg": 0.17,
                    "final_blows_avg": 8.94,
                    "defensive_assists_avg": 1.0,
                    "damage_done_avg": 11857.0,
                    "deaths_avg": 9.64,
                    "objective_time_avg": 0.021666666666666667,
                    "offensive_assists_avg": 0.0,
                    "solo_kills_avg": 1.7,
                    "time_spent_on_fire_avg": 0.02,
                    "objective_kills_avg": 7.11
                }
            },
            "quickplay": {
                "overall_stats": {
                    "win_rate": 0,
                    "level": 20,
                    "prestige": 1,
                    "avatar": "https://blzgdapipro-a.akamaihd.net/game/unlocks/0x0250000000000BBA.png",
                    "wins": 373,
                    "games": null,
                    "comprank": 2395,
                    "losses": null,
                    "endorsement_level": 2,
                    "endorsement_shotcaller": 0,
                    "endorsement_sportsmanship": 0,
                    "endorsement_teammate": 0,
                    "rank_image": "https://d1u1mce87gyfbn.cloudfront.net/game/playerlevelrewards/0x025000000000092A_Border.png",
                    "tier": null
                },
                "game_stats": {
                    "objective_kills": 3127.0,
                    "games_won": 373.0,
                    "objective_kills_most_in_game": 24.0,
                    "melee_final_blows_most_in_game": 3.0,
                    "time_spent_on_fire_most_in_game": 0.1825,
                    "healing_done": 635470.0,
                    "offensive_assists": 202.0,
                    "final_blows_most_in_game": 23.0,
                    "objective_time": 7.751944444444445,
                    "melee_final_blows": 99.0,
                    "medals": 1866.0,
                    "cards": 220.0,
                    "multikill_best": 4.0,
                    "defensive_assists": 586.0,
                    "recon_assists": 17.0,
                    "multikills": 65.0,
                    "defensive_assists_most_in_game": 15.0,
                    "offensive_assists_most_in_game": 12.0,
                    "damage_done": 3509708.0,
                    "teleporter_pads_destroyed": 28.0,
                    "medals_silver": 649.0,
                    "medals_gold": 604.0,
                    "healing_done_most_in_game": 12482.0,
                    "environmental_kills": 86.0,
                    "medals_bronze": 613.0,
                    "solo_kills": 1632.0,
                    "time_spent_on_fire": 10.516944444444444,
                    "eliminations_most_in_game": 39.0,
                    "final_blows": 4660.0,
                    "time_played": 94.0,
                    "environmental_deaths": 139.0,
                    "solo_kills_most_in_game": 23.0,
                    "damage_done_most_in_game": 15485.0,
                    "kpd": 1.74,
                    "eliminations": 8743.0,
                    "objective_time_most_in_game": 0.06472222222222222,
                    "deaths": 5028.0
                },
                "competitive": false,
                "average_stats": {
                    "healing_done_avg": 879.0,
                    "eliminations_avg": 12.09,
                    "melee_final_blows_avg": 0.13,
                    "final_blows_avg": 6.44,
                    "defensive_assists_avg": 1.0,
                    "damage_done_avg": 4854.0,
                    "deaths_avg": 6.95,
                    "objective_time_avg": 0.010555555555555556,
                    "offensive_assists_avg": 0.0,
                    "solo_kills_avg": 2.25,
                    "time_spent_on_fire_avg": 0.014444444444444446,
                    "objective_kills_avg": 4.32
                }
            }
        },
        "heroes": {
            "stats": {
                "quickplay": { },
                "competitive": { }
            },
            "playtime": {
                "quickplay": { },
                "competitive": { }
            }
        },
        "achievements": { }
    },
    "any": null

}
```

### `GET /api/v3/u/:battletag/achievements`
**Get user achievements status.**

*Example:*

`https://owapi.net/api/v3/u/Dad-12262/achievements`

*Result:*

This is a mapping of category -> hash which is another mapping of achievement -> unlocked (True/False).

```json
{

    "_request": {
        "api_ver": 3,
        "route": "/api/v3/u/Dad-12262/achievements"
    },
    "kr": null,
    "eu": null,
    "us": {
        "stats": { },
        "heroes": {
            "stats": {
                "quickplay": { },
                "competitive": { }
            },
            "playtime": {
                "quickplay": { },
                "competitive": { }
            }
        },
        "achievements": {
            "defense": {
                "ice_blocked": true,
                "triple_threat": false,
                "simple_geometry": false,
                "the_dragon_is_sated": false,
                "did_that_sting": true,
                "mine_like_a_steel_trap": true,
                "charge": false,
                "cold_snap": false,
                "raid_wipe": true,
                "armor_up": true,
                "roadkill": true,
                "smooth_as_silk": true
            },
            "offense": {
                "whoa_there": true,
                "die_die_die_die": false,
                "its_high_noon": false,
                "their_own_worst_enemy": false,
                "clearing_the_area": true,
                "target_rich_environment": true,
                "death_from_above": false,
                "total_recall": true,
                "rocket_man": false,
                "slice_and_dice": false,
                "special_delivery": false,
                "waste_not_want_not": false
            },
            "support": {
                "rapid_discord": false,
                "enabler": false,
                "huge_rez": true,
                "supersonic": true,
                "naptime": false,
                "huge_success": false,
                "the_iris_embraces_you": false,
                "the_car_wash": true,
                "the_floor_is_lava": false,
                "group_health_plan": true
            },
            "general": {
                "decorated": true,
                "blackjack": true,
                "centenary": true,
                "undying": true,
                "level_10": true,
                "the_path_is_closed": true,
                "level_50": true,
                "level_25": true,
                "decked_out": false,
                "survival_expert": false,
                "the_friend_zone": true
            },
            "tank": {
                "i_am_your_shield": true,
                "mine_sweeper": false,
                "storm_earth_and_fire": false,
                "giving_you_the_hook": true,
                "power_overwhelming": true,
                "anger_management": false,
                "hog_wild": true,
                "the_power_of_attraction": true,
                "shot_down": false,
                "game_over": false
            },
            "maps": {
                "world_traveler": true,
                "lockdown": true,
                "cant_touch_this": true,
                "shutout": true,
                "escort_duty": true,
                "double_cap": true
            }
        }
    },
    "any": null

}
```

### `GET /api/v3/u/:battletag/heroes`
**Get user hero stats**

*Example:*

`https://owapi.net/api/v3/u/Dad-12262/heroes`

*Result:*

The `heroes` key will contain two subkeys, inside the respective `quickplay` and `competitive` subkeys:

   - `stats`, which signifies specific hero stats.

    - Each hero that the user has played will have a key with the hero specific fields from the PlayOverwatch website
    inside a hash mapping here.

   - `playtime`, which signifies specific hero playtime.

    - Each hero will have a key and the play time in hours inside a hash mapping here.

```json
{

    "_request": {
        "api_ver": 3,
        "route": "/api/v3/u/Dad-12262/heroes"
    },
    "kr": null,
    "eu": null,
    "us": {
        "stats": { },
        "heroes": {
            "stats": {
                "quickplay": {
                    "junkrat": {
                        "general_stats": {
                            "objective_kills": 273.0,
                            "overwatch.guid.0x0860000000000031": 2161.0,
                            "objective_kills_most_in_game": 15.0,
                            "medals_gold": 53.0,
                            "eliminations_most_in_life": 11.0,
                            "final_blows_most_in_game": 20.0,
                            "melee_final_blow": 1.0,
                            "overwatch.guid.0x08600000000001bb": "60%",
                            "cards": 9.0,
                            "multikill_best": 4.0,
                            "overwatch.guid.0x086000000000033d": 59.0,
                            "eliminations_per_life": 1.8,
                            "multikills": 4.0,
                            "kill_streak_best": 11.0,
                            "eliminations_most_in_game": 29.0,
                            "damage_done": 425330.0,
                            "teleporter_pads_destroyed": 3.0,
                            "medals_silver": 54.0,
                            "damage_done_most_in_life": 7125.0,
                            "objective_time": "18:56",
                            "environmental_kills": 2.0,
                            "weapon_accuracy": "23%",
                            "medals_bronze": 45.0,
                            "solo_kills": 225.0,
                            "time_spent_on_fire": "31:21",
                            "medals": 152.0,
                            "final_blows": 536.0,
                            "time_played": "7 hours",
                            "environmental_deaths": 10.0,
                            "solo_kills_most_in_game": 11.0,
                            "overwatch.guid.0x0860000000000030": 9172.0,
                            "damage_done_most_in_game": 11795.0,
                            "games_won": 28.0,
                            "eliminations": 827.0,
                            "objective_time_most_in_game": "01:00",
                            "deaths": 459.0
                        },
                        "hero_stats": {
                            "rip-tire_kills_most_in_game": 9.0,
                            "rip-tire_kills": 129.0,
                            "enemies_trapped": 356.0,
                            "enemies_trapped_most_in_game": 12.0,
                            "enemies_trapped_a_minute": 6.08,
                            "melee_final_blow_most_in_game": 1.0
                        }
                    }
                },
                "competitive": {
                    "junkrat": {
                        "general_stats": {
                            "objective_kills": 13.0,
                            "overwatch.guid.0x0860000000000031": 98.0,
                            "objective_kills_most_in_game": 5.0,
                            "medals_gold": 1.0,
                            "overwatch.guid.0x0860000000000430": 1.0,
                            "eliminations_most_in_life": 5.0,
                            "win_percentage": "69%",
                            "final_blows_most_in_game": 8.0,
                            "objective_time": "00:32",
                            "overwatch.guid.0x08600000000001bb": "80%",
                            "eliminations_per_life": 1.2,
                            "kill_streak_best": 5.0,
                            "eliminations_most_in_game": 10.0,
                            "damage_done": 21895.0,
                            "medals_silver": 2.0,
                            "damage_done_most_in_life": 2414.0,
                            "weapon_accuracy": "27%",
                            "medals_bronze": 1.0,
                            "solo_kills": 5.0,
                            "time_spent_on_fire": "00:10",
                            "medals": 3.0,
                            "final_blows": 16.0,
                            "time_played": "16 minutes",
                            "solo_kills_most_in_game": 2.0,
                            "overwatch.guid.0x0860000000000030": 359.0,
                            "damage_done_most_in_game": 5317.0,
                            "games_played": 2.0,
                            "games_won": 1.0,
                            "eliminations": 24.0,
                            "objective_time_most_in_game": "00:09",
                            "deaths": 20.0
                        },
                        "hero_stats": {
                            "enemies_trapped_a_minute": 8.71,
                            "enemies_trapped": 15.0,
                            "enemies_trapped_most_in_game": 4.0
                        }
                    }
                }
            },
            "playtime": {
                "quickplay": {
                    "junkrat": 7.0,
                    "soldier76": 3.0,
                    "hanzo": 0.8333333333333334,
                    "bastion": 0.3333333333333333,
                    "torbjorn": 6.0,
                    "winston": 6.0,
                    "dva": 0.5166666666666667,
                    "ana": 0,
                    "reinhardt": 16.0,
                    "lucio": 3.0,
                    "pharah": 8.0,
                    "zenyatta": 1.0,
                    "reaper": 0.2833333333333333,
                    "zarya": 7.0,
                    "mercy": 7.0,
                    "symmetra": 4.0,
                    "mccree": 3.0,
                    "widowmaker": 3.0,
                    "mei": 1.0,
                    "tracer": 2.0,
                    "roadhog": 8.0,
                    "genji": 0.26666666666666666
                },
                "competitive": {
                    "junkrat": 0.26666666666666666,
                    "soldier76": 0.03333333333333333,
                    "hanzo": 0,
                    "bastion": 0.01,
                    "torbjorn": 0,
                    "winston": 0.03333333333333333,
                    "dva": 0.0005555555555555556,
                    "ana": 0,
                    "reinhardt": 0.6833333333333333,
                    "lucio": 0.11666666666666667,
                    "pharah": 0.7833333333333333,
                    "mccree": 0,
                    "reaper": 0,
                    "zarya": 0.48333333333333334,
                    "mercy": 0.05,
                    "symmetra": 0,
                    "zenyatta": 0.05,
                    "widowmaker": 0,
                    "mei": 0.016666666666666666,
                    "tracer": 0.05,
                    "roadhog": 0.45,
                    "genji": 0
                }
            }
        },
        "achievements": { }
    },
    "any": null

}
```

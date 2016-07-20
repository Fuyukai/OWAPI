# OWAPI API Docs

##V2

** All times are in *HOURS* unless specified otherwise. **

#### Note about regions&platforms

Regions and platforms can be overriden with URL parameters.

For example, if you wanted to force fetching of US stats:

```
$ http GET "https://owapi.net/api/v2/SunDwarf-21353/stats/general?region=us"
```

This also applies to platforms - you can override the platform with `?platform=<pc|xbox|psn>`.

### `GET /api/v2/u/:battletag/stats`
**Get the basic stats of a user.**

Like all API requests, this will automatically determine the region of the user.

*Example:*

```
$ http GET "https://owapi.net/api/v2/u/z1Ad-1583/stats/general"
```

*Result:*
```
HTTP/1.1 200 OK
Content-Length: 2138
Content-Type: application/json
Date: Sun, 10 Jul 2016 12:16:33 -0000
Server: Kyoukai/1.3.6 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/v2/u/z1Ad-1583/stats/general"
    },
    "battletag": "z1Ad-1583",
    "featured_stats": [
        {
            "avg": 0.16,
            "name": "melee final blows",
            "value": 165.0
        },
        {
            "avg": 6845.0,
            "name": "damage done",
            "value": 6722098.0
        },
        {
            "avg": 1.0,
            "name": "defensive assists",
            "value": 563.0
        },
        {
            "avg": 6.11,
            "name": "objective kills",
            "value": 6005.0
        },
        {
            "avg": 955.0,
            "name": "healing done",
            "value": 937741.0
        },
        {
            "avg": 5.44,
            "name": "deaths",
            "value": 5344.0
        },
        {
            "avg": 0.0,
            "name": "offensive assists",
            "value": 234.0
        },
        {
            "avg": 2.39,
            "name": "solo kills",
            "value": 2348.0
        },
        {
            "avg": 0.029166666666666667,
            "name": "time spent on fire",
            "value": 28.641666666666666
        },
        {
            "avg": 0.012222222222222221,
            "name": "objective time",
            "value": 12.104444444444445
        },
        {
            "avg": 9.5,
            "name": "final blows",
            "value": 9330.0
        },
        {
            "avg": 17.76,
            "name": "eliminations",
            "value": 17450.0
        }
    ],
    "game_stats": {
        "cards": 519.0,
        "damage_done": 6722098.0,
        "damage_done_most_in_game": 25687.0,
        "deaths": 5344.0,
        "defensive_assists": 563.0,
        "defensive_assists_most_in_game": 19.0,
        "eliminations": 17450.0,
        "eliminations_most_in_game": 49.0,
        "environmental_deaths": 58.0,
        "environmental_kills": 62.0,
        "final_blows": 9330.0,
        "final_blows_most_in_game": 34.0,
        "games_played": 982.0,
        "games_won": 654.0,
        "healing_done": 937741.0,
        "healing_done_most_in_game": 11669.0,
        "kpd": 3.27,
        "medals": 3544.0,
        "medals_bronze": 763.0,
        "medals_gold": 1617.0,
        "medals_silver": 1164.0,
        "melee_final_blows": 165.0,
        "melee_final_blows_most_in_game": 5.0,
        "multikill_best": 5.0,
        "multikills": 191.0,
        "objective_kills": 6005.0,
        "objective_kills_most_in_game": 27.0,
        "objective_time": 12.104444444444445,
        "objective_time_most_in_game": 0.065,
        "offensive_assists": 234.0,
        "offensive_assists_most_in_game": 13.0,
        "recon_assists": 6.0,
        "solo_kills": 2348.0,
        "solo_kills_most_in_game": 34.0,
        "teleporter_pads_destroyed": 20.0,
        "time_played": 121.0,
        "time_spent_on_fire": 28.641666666666666,
        "time_spent_on_fire_most_in_game": 0.18472222222222223
    },
    "overall_stats": {
        "comprank": 80,
        "games": 982,
        "level": 86,
        "losses": 328,
        "prestige": 1,
        "rank": null,
        "win_rate": 66,
        "wins": 654
    },
    "region": "us"
}

```

### `GET /api/v2/u/:battletag/stats/competitive`
**Get the basic competitive stats of a user.**

Like all API requests, this will automatically determine the region of the user.

*Example:*

```
$ http GET "https://owapi.net/api/v2/u/Aurelius-1648/stats/competitive"
```

*Result:*
```
HTTP/1.1 200 OK
Content-Length: 2123
Content-Type: application/json
Date: Sun, 10 Jul 2016 12:19:01 -0000
Server: Kyoukai/1.3.6 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/v2/u/Aurelius-1648/stats/general"
    },
    "battletag": "Aurelius-1648",
    "featured_stats": [
        {
            "avg": 0.14,
            "name": "melee final blows",
            "value": 71.0
        },
        {
            "avg": 4637.0,
            "name": "damage done",
            "value": 2337039.0
        },
        {
            "avg": 1.0,
            "name": "defensive assists",
            "value": 372.0
        },
        {
            "avg": 5.49,
            "name": "objective kills",
            "value": 2771.0
        },
        {
            "avg": 747.0,
            "name": "healing done",
            "value": 376474.0
        },
        {
            "avg": 6.66,
            "name": "deaths",
            "value": 3360.0
        },
        {
            "avg": 0.0,
            "name": "offensive assists",
            "value": 80.0
        },
        {
            "avg": 1.59,
            "name": "solo kills",
            "value": 806.0
        },
        {
            "avg": 0.014444444444444446,
            "name": "time spent on fire",
            "value": 7.339444444444444
        },
        {
            "avg": 0.014166666666666666,
            "name": "objective time",
            "value": 7.2525
        },
        {
            "avg": 5.9,
            "name": "final blows",
            "value": 2977.0
        },
        {
            "avg": 11.91,
            "name": "eliminations",
            "value": 6003.0
        }
    ],
    "game_stats": {
        "cards": 192.0,
        "damage_done": 2337039.0,
        "damage_done_most_in_game": 16268.0,
        "deaths": 3360.0,
        "defensive_assists": 372.0,
        "defensive_assists_most_in_game": 18.0,
        "eliminations": 6003.0,
        "eliminations_most_in_game": 37.0,
        "environmental_deaths": 108.0,
        "environmental_kills": 32.0,
        "final_blows": 2977.0,
        "final_blows_most_in_game": 20.0,
        "games_played": 504.0,
        "games_won": 256.0,
        "healing_done": 376474.0,
        "healing_done_most_in_game": 9994.0,
        "kpd": 1.79,
        "medals": 1393.0,
        "medals_bronze": 381.0,
        "medals_gold": 530.0,
        "medals_silver": 482.0,
        "melee_final_blows": 71.0,
        "melee_final_blows_most_in_game": 4.0,
        "multikill_best": 5.0,
        "multikills": 62.0,
        "objective_kills": 2771.0,
        "objective_kills_most_in_game": 30.0,
        "objective_time": 7.2525,
        "objective_time_most_in_game": 0.06916666666666667,
        "offensive_assists": 80.0,
        "offensive_assists_most_in_game": 5.0,
        "recon_assists": 2.0,
        "solo_kills": 806.0,
        "solo_kills_most_in_game": 20.0,
        "teleporter_pads_destroyed": 2.0,
        "time_played": 65.0,
        "time_spent_on_fire": 7.339444444444444,
        "time_spent_on_fire_most_in_game": 0.19027777777777777
    },
    "overall_stats": {
        "comprank": 53,
        "games": 504,
        "level": 81,
        "losses": 248,
        "prestige": null,
        "rank": null,
        "win_rate": 50,
        "wins": 256
    },
    "region": "us"
}

```

### `GET /api/v2/u/:battletag/heroes/:heroname`

**Get detailed information about a player's performance as a hero.**

Note that hero names do not have special characters (lucio not lúcio) and
are lowercase. Use `d.va` or `dva` for D.va and `s76` or `soldier76` for S76.

*Example*:
```
$ http GET "https://owapi.net/api/v2/u/Aurelius-1648/heroes/reinhardt"
```

*Result*:

```
{
    "hero_stats": {
        "damage_blocked_most_in_game": 27137.0,
        "charge_kills": 385.0,
        "fire_strike_kills_most_in_game": 13.0,
        "earthshatter_kills": 487.0,
        "charge_kills_most_in_game": 9.0,
        "damage_blocked": 2046918.0,
        "earthshatter_kills_most_in_game": 9.0,
        "fire_strike_kills": 690.0
    },
    "battletag": "Aurelius-1648",
    "_request": {
        "api_ver": 1,
        "route": "/api/v2/u/Aurelius-1648/heroes/reinhardt"
    },
    "general_stats": {
        "games_won": 104.0,
        "medals_gold": 204.0,
        "eliminations": 2279.0,
        "damage_done": 882436.0,
        "multikill_best": 5.0,
        "medals_bronze": 139.0,
        "eliminations_most_in_life": 18.0,
        "medals": 513.0,
        "games_played": 197.0,
        "eliminations_per_life": 1.65,
        "objective_time": 13426.0,
        "time_spent_on_fire": 12365.0,
        "final_blows_most_in_game": 20.0,
        "medals_silver": 171.0,
        "solo_kills": 335.0,
        "time_played": "25 hours",
        "teleporter_pads_destroyed": 1.0,
        "eliminations_most_in_game": 33.0,
        "environmental_kills": 13.0,
        "environmental_deaths": 40.0,
        "damage_done_most_in_life": 5630.0,
        "objective_time_most_in_game": 249.0,
        "cards": 91.0,
        "objective_kills_most_in_game": 17.0,
        "multikills": 33.0,
        "win_percentage": "52%",
        "final_blows": 1340.0,
        "solo_kills_most_in_game": 6.0,
        "damage_done_most_in_game": 13569.0,
        "deaths": 1378.0,
        "objective_kills": 957.0
    },
    "region": "us"
}
```

##V1


### `GET /api/v1/u/:battletag/stats`
***Deprecated - use /api/v2/u/:battletag/stats.***
**Get the basic stats of a user.**

Like all API requests, this will automatically determine the region of the user.

*Example:*

```
$ http GET "https://owapi.net/api/v1/u/SunDwarf-21353/stats"
```

*Result:*
```
{HTTP/1.1 200 OK
Content-Length: 584
Content-Type: application/json
Date: Thu, 30 Jun 2016 18:45:56 -0000
Server: Kyoukai/1.3.1 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/v1/u/SunDwarf-21353/stats"
    },
    "battletag": "SunDwarf-21353",
    "game_stats": [
        {
            "avg": 5.44,
            "name": "final blows",
            "value": 441
        },
        {
            "avg": 9.73,
            "name": "eliminations",
            "value": 788
        },
        {
            "avg": null,
            "name": "kpd",
            "value": 1.6659619450317125
        },
        {
            "avg": 5.84,
            "name": "deaths",
            "value": 473
        },
        {
            "avg": 3756.0,
            "name": "damage",
            "value": 304242
        },
        {
            "avg": 609.95,
            "name": "healing",
            "value": 49406
        },
        {
            "avg": 2.2,
            "name": "medals",
            "value": 178
        }
    ],
    "overall_stats": {
        "games": 81,
        "level": 19,
        "losses": 41,
        "winrate": 49.38,
        "wins": 40
    },
    "region": "eu"
}
```

### `GET /api/v1/u/:battletag/heroes`

**Get the played heroes of a user.**

This is ordered by your play time.

*Example:*

```
$ http GET "https://owapi.net/api/v1/u/SunDwarf-21353/heroes"
```

*Result:*
```
HTTP/1.1 200 OK
Content-Length: 2162
Content-Type: application/json
Date: Tue, 05 Jul 2016 10:58:53 -0000
Server: Kyoukai/1.3.1 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/v1/u/SunDwarf-21353/heroes"
    },
    "battletag": "SunDwarf-21353",
    "heroes": [
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/11",
            "games": 26,
            "hours": 2.0,
            "kpd": 2.12,
            "losses": 12,
            "name": "pharah",
            "winrate": 54.0,
            "wins": 14
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/12",
            "games": 18,
            "hours": 1.0,
            "kpd": 1.25,
            "losses": 11,
            "name": "reinhardt",
            "winrate": 39.0,
            "wins": 7
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/22",
            "games": 8,
            "hours": 0.7,
            "kpd": 3.52,
            "losses": 3,
            "name": "d.va",
            "winrate": 63.0,
            "wins": 5
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/3",
            "games": 6,
            "hours": 0.467,
            "kpd": 1.91,
            "losses": 2,
            "name": "lúcio",
            "winrate": 67.0,
            "wins": 4
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/9",
            "games": 4,
            "hours": 0.383,
            "kpd": 1.55,
            "losses": 1,
            "name": "widowmaker",
            "winrate": 75.0,
            "wins": 3
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/17",
            "games": 4,
            "hours": 0.4,
            "kpd": 0.25,
            "losses": 1,
            "name": "mercy",
            "winrate": 75.0,
            "wins": 3
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/7",
            "games": 3,
            "hours": 0.417,
            "kpd": 1.09,
            "losses": 3,
            "name": "tracer",
            "winrate": 0.0,
            "wins": 0
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/6",
            "games": 3,
            "hours": 0.467,
            "kpd": 1.19,
            "losses": 1,
            "name": "mccree",
            "winrate": 67.0,
            "wins": 2
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/16",
            "games": 3,
            "hours": 0.45,
            "kpd": 1.24,
            "losses": 2,
            "name": "hanzo",
            "winrate": 33.0,
            "wins": 1
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/4",
            "games": 2,
            "hours": 0.15,
            "kpd": 1.21,
            "losses": 2,
            "name": "soldier: 76",
            "winrate": 0.0,
            "wins": 0
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/8",
            "games": 1,
            "hours": 0.067,
            "kpd": 2.0,
            "losses": 1,
            "name": "reaper",
            "winrate": 0.0,
            "wins": 0
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/15",
            "games": 1,
            "hours": 0.083,
            "kpd": 2.0,
            "losses": 0,
            "name": "bastion",
            "winrate": 100.0,
            "wins": 1
        },
        {
            "extended_url": "/api/v1/u/SunDwarf-21353/heroes/14",
            "games": 1,
            "hours": 0.15,
            "kpd": 0.83,
            "losses": 1,
            "name": "torbjörn",
            "winrate": 0.0,
            "wins": 0
        }
    ],
    "region": "eu"
}

```
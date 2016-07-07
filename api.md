# OWAPI API Docs

##V2

### `GET /api/v2/u/:battletag/stats`
**Get the basic stats of a user.**

Like all API requests, this will automatically determine the region of the user.

*Example:*

```
$ http GET "https://owapi.net/api/v2/u/SunDwarf-21353/stats"
```

*Result:*
```
HTTP/1.1 200 OK
Content-Length: 1303
Content-Type: application/json
Date: Thu, 30 Jun 2016 18:45:35 -0000
Server: Kyoukai/1.3.1 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/v2/u/SunDwarf-21353/stats"
    },
    "battletag": "SunDwarf-21353",
    "game_stats": {
        "cards": 25.0,
        "damage_done": 304242.0,
        "damage_done_most_in_game": 13303.0,
        "deaths": 473.0,
        "defensive_assists": 39.0,
        "defensive_assists_most_in_game": 11.0,
        "eliminations": 788.0,
        "eliminations_most_in_game": 26.0,
        "environmental_deaths": 12.0,
        "environmental_kills": 8.0,
        "final_blows": 441.0,
        "final_blows_most_in_game": 16.0,
        "games_played": 81.0,
        "games_won": 40.0,
        "healing_done": 49406.0,
        "healing_done_most_in_game": 7832.0,
        "kpd": 1.67,
        "medals": 178.0,
        "medals_bronze": 59.0,
        "medals_gold": 60.0,
        "medals_silver": 59.0,
        "melee_final_blows": 4.0,
        "melee_final_blows_most_in_game": 2.0,
        "multikill_best": 3.0,
        "multikills": 3.0,
        "objective_kills": 228.0,
        "objective_kills_most_in_game": 10.0,
        "objective_time": "34:58",
        "objective_time_most_in_game": "01:37",
        "offensive_assists": 13.0,
        "offensive_assists_most_in_game": 7.0,
        "recon_assists": 9.0,
        "recon_assists_most_in_game": 1.0,
        "score": 72687.0,
        "solo_kills": 173.0,
        "solo_kills_most_in_game": 16.0,
        "time_played": "10 hours",
        "time_spent_on_fire": "34:57",
        "time_spent_on_fire_most_in_game": "04:52"
    },
    "overall_stats": {
        "games": 81,
        "level": 19,
        "losses": 41,
        "rank": null,
        "win_rate": 49,
        "wins": 40
    },
    "region": "eu"
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
{
    "battletag": "Aurelius-1648",
    "_request": {
        "api_ver": 1,
        "route": "/api/v2/u/Aurelius-1648/stats/competitive"
    },
    "game_stats": {
        "environmental_deaths": 9.0,
        "games_won": 10.0,
        "medals_gold": 19.0,
        "eliminations": 412.0,
        "damage_done": 201970.0,
        "multikill_best": 4.0,
        "time_spent_on_fire": "35:03",
        "medals_bronze": 23.0,
        "healing_done": 37755.0,
        "offensive_assists": 4.0,
        "eliminations_most_in_game": 39.0,
        "medals_silver": 15.0,
        "objective_time": "32:33",
        "healing_done_most_in_game": 10380.0,
        "offensive_assists_most_in_game": 3.0,
        "final_blows_most_in_game": 22.0,
        "medals": 57.0,
        "environmental_kills": 2.0,
        "time_played": "5 hours",
        "teleporter_pads_destroyed": 1.0,
        "melee_final_blows": 2.0,
        "melee_final_blows_most_in_game": 1.0,
        "solo_kills": 40.0,
        "defensive_assists_most_in_game": 25.0,
        "recon_assists": 2.0,
        "objective_time_most_in_game": "03:22",
        "cards": 5.0,
        "objective_kills_most_in_game": 21.0,
        "multikills": 5.0,
        "defensive_assists": 45.0,
        "kpd": 1.55,
        "games_played": 27.0,
        "final_blows": 212.0,
        "time_spent_on_fire_most_in_game": "07:23",
        "solo_kills_most_in_game": 22.0,
        "damage_done_most_in_game": 18981.0,
        "deaths": 265.0,
        "objective_kills": 197.0
    },
    "region": "us",
    "overall_stats": {
        "games": 27,
        "comprank": 54,
        "rank": null,
        "level": 80,
        "losses": 17,
        "wins": 10,
        "win_rate": 37
    }
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
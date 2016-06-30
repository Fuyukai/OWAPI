# OWAPI API Docs

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

**Get the top 5 played heroes of a user.**

There is not currently a way to get heroes past the top 5.

*Example:*

```
$ http GET "https://owapi.net/api/v1/u/SunDwarf-21353/heroes"
```

*Result:*
```
HTTP/1.1 200 OK
Content-Length: 691
Content-Type: application/json
Date: Mon, 30 May 2016 21:40:17 -0000
Server: Kyoukai/1.3.0 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/v1/u/SunDwarf-21353/heroes"
    },
    "battletag": "SunDwarf-21353",
    "heroes": [
        {
            "extended_url": "/api/u/SunDwarf-21353/heroes/11",
            "games": 19,
            "kpd": 2.2,
            "name": "pharah",
            "winrate": 52.6
        },
        {
            "extended_url": "/api/u/SunDwarf-21353/heroes/16",
            "games": 3,
            "kpd": 1.24,
            "name": "hanzo",
            "winrate": 33.3
        },
        {
            "extended_url": "/api/u/SunDwarf-21353/heroes/22",
            "games": 3,
            "kpd": 2.86,
            "name": "d.va",
            "winrate": 66.7
        },
        {
            "extended_url": "/api/u/SunDwarf-21353/heroes/12",
            "games": 2,
            "kpd": 0.86,
            "name": "reinhardt",
            "winrate": 0.0
        },
        {
            "extended_url": "/api/u/SunDwarf-21353/heroes/6",
            "games": 2,
            "kpd": 0.88,
            "name": "mccree",
            "winrate": 50.0
        }
    ],
    "region": "eu"
}
```

### `GET /api/v1/u/:battletag/heroes/:id`

**Get detailed information about a player's performance as a hero.**

*Example*:
```
$ http GET "https://owapi.net/api/v1/u/SunDwarf-21353/heroes/11"
```

*Result*:

```
HTTP/1.1 200 OK
Content-Length: 1843
Content-Type: application/json
Date: Mon, 30 May 2016 21:41:17 -0000
Server: Kyoukai/1.3.0 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/v1/u/SunDwarf-21353/heroes/11"
    },
    "battletag": "SunDwarf-21353",
    "region": "eu",
    "stats": [
        {
            "name": "hero-specific stats",
            "stats": [
                {
                    "name": "average barrage kills",
                    "value": 1.0
                },
                {
                    "name": "average rocket direct hits",
                    "value": 28.0
                },
                {
                    "name": "best barrage kills",
                    "value": 4.0
                },
                {
                    "name": "best rocket direct hits",
                    "value": 74.0
                },
                {
                    "name": "total barrage kills",
                    "value": 12.0
                },
                {
                    "name": "total rocket direct hits",
                    "value": 542.0
                }
            ]
        },
        {
            "name": "overall",
            "stats": [
                {
                    "name": "final blows",
                    "value": 148.0
                },
                {
                    "name": "eliminations",
                    "value": 235.0
                },
                {
                    "name": "deaths",
                    "value": 107.0
                },
                {
                    "name": "damage done",
                    "value": 98981.0
                },
                {
                    "name": "score",
                    "value": 15944.0
                },
                {
                    "name": "melee kills",
                    "value": 0.0
                },
                {
                    "name": "time played",
                    "value": "2 hours"
                },
                {
                    "name": "time on fire",
                    "value": "7 minutes"
                },
                {
                    "name": "objective kills",
                    "value": 47.0
                },
                {
                    "name": "objective time",
                    "value": "4 minutes"
                },
                {
                    "name": "accuracy",
                    "value": "52%"
                },
                {
                    "name": "medals earned",
                    "value": 41.0
                },
                {
                    "name": "cards earned",
                    "value": 10.0
                }
            ]
        },
        {
            "name": "averages per game",
            "stats": [
                {
                    "name": "final blows",
                    "value": 7.69
                },
                {
                    "name": "eliminations",
                    "value": 12.22
                },
                {
                    "name": "deaths",
                    "value": 5.56
                },
                {
                    "name": "damage done",
                    "value": 5149.0
                },
                {
                    "name": "objective kills",
                    "value": 2.44
                },
                {
                    "name": "objective time",
                    "value": "13.12 seconds"
                }
            ]
        },
        {
            "name": "best in one game",
            "stats": [
                {
                    "name": "final blows",
                    "value": 15.0
                },
                {
                    "name": "eliminations",
                    "value": 26.0
                },
                {
                    "name": "killstreak",
                    "value": 12.0
                },
                {
                    "name": "damage done",
                    "value": 13303.0
                },
                {
                    "name": "objective kills",
                    "value": 8.0
                },
                {
                    "name": "objective time",
                    "value": 37.0
                },
                {
                    "name": "accuracy",
                    "value": "69%"
                }
            ]
        },
        {
            "name": "best in one life",
            "stats": [
                {
                    "name": "eliminations",
                    "value": 12.0
                },
                {
                    "name": "damage done",
                    "value": 3481.0
                },
                {
                    "name": "score",
                    "value": 1077.0
                }
            ]
        }
    ]
}
```

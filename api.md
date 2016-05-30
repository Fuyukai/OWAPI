# OWAPI API Docs

### `GET /api/u/:battletag/stats`

**Get the basic stats of a user.**

Like all API requests, this will automatically determine the region of the user.

*Example:*

```
$ http GET "http://127.0.0.1:4444/api/u/SunDwarf-21353/stats"
```

*Result:*
```
HTTP/1.1 200 OK
Content-Length: 577
Content-Type: application/json
Date: Mon, 30 May 2016 21:12:03 -0000
Server: Kyoukai/1.3.0 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/u/SunDwarf-21353/stats"
    },
    "battletag": "SunDwarf-21353",
    "game_stats": [
        {
            "avg": 6.57,
            "name": "final blows",
            "value": 197
        },
        {
            "avg": 10.7,
            "name": "eliminations",
            "value": 321
        },
        {
            "avg": null,
            "name": "kpd",
            "value": 1.9454545454545455
        },
        {
            "avg": 5.5,
            "name": "deaths",
            "value": 165
        },
        {
            "avg": 4354.0,
            "name": "damage",
            "value": 130631
        },
        {
            "avg": 0.0,
            "name": "multikills",
            "value": 0
        },
        {
            "avg": 1.9,
            "name": "medals",
            "value": 57
        }
    ],
    "overall_stats": {
        "games": 30,
        "losses": 16,
        "rank": 46789,
        "win_rate": 46.7,
        "wins": 14
    },
    "region": "eu"
}
```

### `GET /api/u/:battletag/heroes`

**Get the top 5 played heroes of a user.**

There is not currently a way to get heroes past the top 5.

*Example:*

```
$ http GET "http://127.0.0.1:4444/api/u/SunDwarf-21353/heroes"
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
        "route": "/api/u/SunDwarf-21353/heroes"
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

### `GET http://127.0.0.1:4444/api/u/:battletag/heroes/:id`

**Get detailed information about a player's performance as a hero.**

*Example*:
```
$ http GET "http://127.0.0.1:4444/api/u/SunDwarf-21353/heroes/11"
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
        "route": "/api/u/SunDwarf-21353/heroes/11"
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

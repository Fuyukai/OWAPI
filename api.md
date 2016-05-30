# OWAPI API Docs

## `GET /api/u/:battletag/stats`

**Get the basic stats of a user.**

Like all API requests, this will automatically determine the region of the user.

*Example: *

```
$ http GET "http://127.0.0.1:4444/api/u/SunDwarf-21353/stats"
```

*Result: *
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
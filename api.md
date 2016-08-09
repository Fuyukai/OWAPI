# OWAPI API Docs

##V2

** All times are in *HOURS* unless specified otherwise. **

#### Note about Regions & Platforms

Regions and platforms can be overriden with URL parameters.

For example, if you wanted to force fetching of US stats:

```
$ http GET "https://owapi.net/api/v2/u/SunDwarf-21353/stats/general?region=us"
```

Note that if they are not overriden, the API will automatically determine which region to use.

This also applies to platforms - you can override the platform with `?platform=<pc|xbl|psn>`. This defaults to `pc`.

### `GET /api/v2/u/:battletag/stats`
**Get the basic stats of a user.**

*Example:*

```
$ http GET "https://owapi.net/api/v2/u/SunDwarf-21353/stats/general"
```

*Result:*
```
HTTP/1.1 200 OK
Content-Length: 1788
Content-Type: application/json
Date: Wed, 20 Jul 2016 17:19:37 -0000
Server: Kyoukai/1.3.8 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/v2/u/SunDwarf-21353/stats/general"
    },
    "average_stats": {
        "damage_done_avg": 3987.0,
        "deaths_avg": 5.68,
        "defensive_assists_avg": 0.0,
        "eliminations_avg": 10.47,
        "final_blows_avg": 6.12,
        "healing_done_avg": 589.0,
        "melee_final_blows_avg": 0.03,
        "objective_kills_avg": 3.06,
        "objective_time_avg": 0.007222222222222223,
        "offensive_assists_avg": 0.0,
        "solo_kills_avg": 2.3,
        "time_spent_on_fire_avg": 0.008055555555555555
    },
    "battletag": "SunDwarf-21353",
    "game_stats": {
        "cards": 36.0,
        "damage_done": 478462.0,
        "damage_done_most_in_game": 13303.0,
        "deaths": 682.0,
        "defensive_assists": 39.0,
        "defensive_assists_most_in_game": 11.0,
        "eliminations": 1257.0,
        "eliminations_most_in_game": 26.0,
        "environmental_deaths": 12.0,
        "environmental_kills": 8.0,
        "final_blows": 735.0,
        "final_blows_most_in_game": 16.0,
        "games_played": 120.0,
        "games_won": 59.0,
        "healing_done": 70670.0,
        "healing_done_most_in_game": 7832.0,
        "kpd": 1.84,
        "medals": 304.0,
        "medals_bronze": 102.0,
        "medals_gold": 100.0,
        "medals_silver": 102.0,
        "melee_final_blows": 4.0,
        "melee_final_blows_most_in_game": 2.0,
        "multikill_best": 3.0,
        "multikills": 5.0,
        "objective_kills": 368.0,
        "objective_kills_most_in_game": 10.0,
        "objective_time": 0.8880555555555555,
        "objective_time_most_in_game": 0.026944444444444444,
        "offensive_assists": 13.0,
        "offensive_assists_most_in_game": 7.0,
        "recon_assists": 9.0,
        "solo_kills": 277.0,
        "solo_kills_most_in_game": 16.0,
        "time_played": 15.0,
        "time_spent_on_fire": 0.9961111111111111,
        "time_spent_on_fire_most_in_game": 0.08833333333333333
    },
    "overall_stats": {
        "avatar": "https://blzgdapipro-a.akamaihd.net/game/unlocks/0x02500000000008E8.png",
        "comprank": null,
        "games": 120,
        "level": 24,
        "losses": 61,
        "prestige": 0,
        "win_rate": 49,
        "wins": 59
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
HTTP/1.1 200 OK
Content-Length: 1811
Content-Type: application/json
Date: Wed, 20 Jul 2016 17:24:06 -0000
Server: Kyoukai/1.3.6 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/v2/u/Aurelius-1648/stats/competitive"
    },
    "average_stats": {
        "damage_done_avg": 7469.0,
        "deaths_avg": 10.35,
        "defensive_assists_avg": 2.0,
        "eliminations_avg": 16.16,
        "final_blows_avg": 8.37,
        "healing_done_avg": 1440.0,
        "melee_final_blows_avg": 0.1,
        "objective_kills_avg": 7.43,
        "objective_time_avg": 0.02027777777777778,
        "offensive_assists_avg": 0.0,
        "solo_kills_avg": 1.78,
        "time_spent_on_fire_avg": 0.01972222222222222
    },
    "battletag": "Aurelius-1648",
    "game_stats": {
        "cards": 5.0,
        "damage_done": 276363.0,
        "damage_done_most_in_game": 22155.0,
        "deaths": 383.0,
        "defensive_assists": 62.0,
        "defensive_assists_most_in_game": 25.0,
        "eliminations": 598.0,
        "eliminations_most_in_game": 50.0,
        "environmental_deaths": 12.0,
        "environmental_kills": 4.0,
        "final_blows": 310.0,
        "final_blows_most_in_game": 24.0,
        "games_played": 37.0,
        "games_won": 15.0,
        "healing_done": 53276.0,
        "healing_done_most_in_game": 10380.0,
        "kpd": 1.56,
        "medals": 74.0,
        "medals_bronze": 29.0,
        "medals_gold": 23.0,
        "medals_silver": 22.0,
        "melee_final_blows": 4.0,
        "melee_final_blows_most_in_game": 2.0,
        "multikill_best": 4.0,
        "multikills": 8.0,
        "objective_kills": 275.0,
        "objective_kills_most_in_game": 27.0,
        "objective_time": 0.7519444444444444,
        "objective_time_most_in_game": 0.05611111111111111,
        "offensive_assists": 13.0,
        "offensive_assists_most_in_game": 7.0,
        "recon_assists": 2.0,
        "solo_kills": 66.0,
        "solo_kills_most_in_game": 24.0,
        "teleporter_pad_destroyed": 1.0,
        "time_played": 7.0,
        "time_spent_on_fire": 0.7347222222222223,
        "time_spent_on_fire_most_in_game": 0.12305555555555556
    },
    "overall_stats": {
        "avatar": "https://blzgdapipro-a.akamaihd.net/game/unlocks/0x02500000000008C1.png",
        "comprank": 52,
        "games": 37,
        "level": 83,
        "losses": 22,
        "prestige": 0,
        "win_rate": 40,
        "wins": 15
    },
    "region": "us"
}


```

### `GET /api/v2/u/:battletag/heroes`

**Get the list of heroes that a person has played as, and the time.**

*Example*:
```
$ http GET https://owapi.net/api/v2/u/SunDwarf-21353/heroes
```

*Result*:

```
HTTP/1.1 200 OK
Content-Length: 619
Content-Type: application/json
Date: Wed, 20 Jul 2016 17:19:21 -0000
Server: Kyoukai/1.3.6 (see https://github.com/SunDwarf/Kyoukai)

{
    "_request": {
        "api_ver": 1,
        "route": "/api/v2/u/SunDwarf-21353/heroes"
    },
    "battletag": "SunDwarf-21353",
    "heroes": {
        "ana": 0,
        "bastion": 0.2833333333333333,
        "dva": 1.0,
        "genji": 0.1,
        "hanzo": 0.4666666666666667,
        "junkrat": 0.9333333333333333,
        "lucio": 0.85,
        "mccree": 0.7333333333333333,
        "mei": 0.4166666666666667,
        "mercy": 0.38333333333333336,
        "pharah": 3.0,
        "reaper": 0.25,
        "reinhardt": 2.0,
        "roadhog": 0.16666666666666666,
        "soldier76": 1.0,
        "symmetra": 0.010277777777777778,
        "torbjorn": 0.08333333333333333,
        "tracer": 0.4,
        "widowmaker": 0.7333333333333333,
        "winston": 0,
        "zarya": 0,
        "zenyatta": 0.05
    },
    "region": "eu"
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

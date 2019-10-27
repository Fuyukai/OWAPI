## OW API

[Donate to keep OWAPI alive](https://www.patreon.com/sundwarf)

This server is a simple way to get read-only information about player statistics in the game
Overwatch by Blizzard.

**A live version runs on https://owapi.net.**  

## Game data

This API does not aim to expose data about the heroes, maps, etc in the game. For that, use 
https://github.com/jamesmcfadden/overwatch-api. 
 
## API Docs

OWAPI has a very simple RESTful API to get information.  
As the API is read-only, the only method required is `GET`.  

See the [doc](/api.md) for more information. 


### Running an instance

OWAPI has a few requirements:

 - A Python version >3.6
 - Probably a Linux-based server; I don't know about the viability of running it on Windows.
 
**Installation steps:**

 1. **Clone the repository.**
 
     `git clone https://github.com/Fuyukai/OWAPI.git`
     
 2. **Setup a Redis server.**
 
     Redis should be running on the default port - 6379. You can override this in config.yml;
     however.
     Redis is used for caching lots of data so that there's not a 10 second delay on
     EVERY request as the data is fetched and scraped; it is essential.
     
     For Debian/Ubuntu, you can install one with:
     `sudo apt install redis-server`
     
     You can enable it with:
     `sudo systemctl enable redis-server && sudo systemctl start redis-server`.
     
 4. **Install the requirements.**

     For debian-based systems, run this first:
     `sudo apt install libxslt-dev python3-dev python3-venv build-essential zlib1g-dev pkg-config`
     
     Install poetry packaging and dependency manager by following the [installation documentation](https://poetry.eustace.io/docs/#installation).
     
     To set up the virtualenv:
     `poetry install`

 5. **Copy and tweak the example config file.**

    `cp config.example.yml config.yml`
     
 6. **Start the OWAPI server.**
 
     `PYTHONPATH=. poetry run asphalt run config.yml`
     
     The server is now running on http://localhost:4444/
          
     Note: If you want the full speedups from Kyoukai you must run with uvloop enabled:
     `PYTHONPATH=. poetry run asphalt run -l uvloop config.yml`

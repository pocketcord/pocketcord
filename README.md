# pocketcord

A *tiny* discord api for language agnostic testing.

Pocketcord essentially is a discord api that is meant to run fully offline and can send fake payloads to your bot.


## Installation

Clone the repository and run `poetry install`

To run Pocketcord, run `poetry run python -m pocketcord`

## Usage

Pocketcord is meant to be used as a testing tool for discord bots.

The changes needed to use Pocketcord in your bot are minimal, but depend on your library (and language) of choice.


### Python
#### discatcore

To use Pocketcord with discatcore, you only need to add this line before connecting to the gateway:

```py
http._api_url = "http://localhost:5000"
```

Run Pocketcord `poetry run python -m pocketcord` and start your bot!

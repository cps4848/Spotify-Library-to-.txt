# SaveSpotifyLibrary.py

Saves every playlist on your spotify account to a series of text files.

## Dependencies

### macOS / Linux

###### NOTE: If you are using NixOS, see below.

See poetry's [install instructions](https://python-poetry.org/docs/#installing-with-the-official-installer).

##### Install dependencies

```sh
poetry install
```

### NixOS

This repository only supports flakes. Either allow the `.envrc` (`direnv allow`) or use `nix develop`.

## Usage

#### Setup environment variables

```sh
cp .env.example .env
```

Edit the newly created `.env` file with your favorite editor. You must set your username, Spotify client ID, and Spotify client secret. Optionally, you may set the directory to store the playlists.

#### Run the program

```sh
python SaveSpotifyLibrary.py
```

Execution may take a few minutes if you have a lot of playlists.

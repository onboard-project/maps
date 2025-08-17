# 🗺️ Onboard Maps

This repositories contains the tiles used by the [Onboard Project](https://github.com/onboard-project) maps

This maps, which cover the area between the cities of Milan, IT and Bergamo, IT (the extent of the [Onboard Project](https://github.com/onboard-project)) are sourced from [Protomaps](https://protomaps.com) as pmtiles, stiled and served on localhost using tileserver-gl, then downloaded using a Python script in both light and dark theme.

> [!CAUTION]
> **This is only an educational purpose project (just a few API calls needed), and the tiles are served using GitHub pages.**
> 
> **Please, if you want to access tiles, clone this repo and host/serve on your own.**

## 📷 Why do I use raster tiles instead of vector tiles (lightweight and faster)?

I use raster tiles in my project because it's the only type of tiles flutter\_map supports natively everywhere, while vector tiles are not cross-platform and where available I have found them extremely laggy and unstable.

> [!NOTE]
> **When a working solution will have come out, I will happily switch to vector tiles.**

## 🔃 To update the tiles

> [!TIP]
> 1. Make sure you have globally installed tileserver-gl and protomaps and that you have a virtual python environment in the folder!
>
> 2. To change the area covered by the download, make sure to change it both in `serve_tiles.bat` and `main.py`

To update the tiles, or generate your own, _(in Windows command prompt)_ run `serve_tiles.bat` and when the server is ready (verify at [localhost:8080](http://localhost:8080)) run `download_tiles.bat`.


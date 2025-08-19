# 🗺️ Onboard Maps

>[!Note]
> **EDUCATIONAL PROJECT DISCLAIMER**
>
>This project is developed purely for **educational and demonstrative purposes**. While it aims to provide useful public transport information for Milan, it relies on data sources, including scraping information from `giromilano.atm.it`.
>
>**The terms of service for ATM (Azienda Trasporti Milanesi) regarding data usage are not explicitly clear, and this project may potentially violate them.**
>
>Therefore:
>- **Use at Your Own Risk:** We do not guarantee the accuracy or continued availability of the data, nor do we assume responsibility for any consequences arising from its use.
>- **Unscheduled Discontinuation:** This project, or parts of it, may be taken down or become non-functional unexpectedly if ATM's policies change or if the data sources become inaccessible.
>
>We advise caution and understanding of these limitations.

This repository contains the custom raster tiles and the tools used to generate them for the [Onboard Project](https://github.com/onboard-project) maps. These maps cover the urban area of Milan, Italy, extending towards Bergamo, providing a visually rich and detailed backdrop for transport information.

## 📷 Why Raster Tiles?

We utilize raster tiles in this project because `flutter_map` offers robust and performant native support for them across all target platforms (Windows, Android, Web). While vector tiles are often lighter and faster, their cross-platform compatibility and stability within `flutter_map` are still evolving.

> [!NOTE]
> **Our goal is to switch to vector tiles as soon as a stable and performant cross-platform solution becomes readily available in `flutter_map`.**

## ✨ Key Features

*   **Custom Map Tiles:** Provides a unique visual style tailored for public transport visualization.
*   **Milan & Bergamo Coverage:** Tiles are generated for the specific geographic extent relevant to the Onboard Project.
*   **Light & Dark Themes:** Includes pre-generated tiles for both light and dark UI themes.
*   **Automated Generation:** Contains scripts to automate the process of sourcing, styling, and downloading map tiles.

## ⚠️ Important Considerations

> [!CAUTION]
> **This project serves educational and demonstration purposes. The map tiles are hosted via GitHub Pages, which is NOT designed for high-traffic public tile serving.**
>
> **If you intend to use these tiles in a production environment or for extensive access, please clone this repository and host/serve them on your own infrastructure.**

## 🔄 Updating/Generating Tiles

To update the existing tiles or generate your own custom set:

> [!TIP]
> 1.  Ensure you have `tileserver-gl` and `protomaps` installed globally on your system.
> 2.  Verify that you have a Python virtual environment set up within this repository's folder.
> 3.  If you want to change the geographic area covered by the tiles, remember to adjust the extent in both `serve_tiles.bat` (for `tileserver-gl` bounding box) and `main.py` (for the Python download script).

Follow these steps (_in Windows command prompt_):

1.  **Start the Tile Server:**
    ```bash
    serve_tiles.bat
    ```
    Wait for the server to be ready and verify its availability by navigating to `http://localhost:8080` in your web browser.

2.  **Download the Tiles:**
    While `tileserver-gl` is running, open a new command prompt and run:
    ```bash
    download_tiles.bat
    ```
    This script will connect to your local `tileserver-gl` instance and download the pre-styled raster tiles into the appropriate `light` and `dark` directories.

## 🛠️ Development Setup (Optional)

If you need to delve into the Python script or batch files:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/onboard-project/maps.git
    cd maps
    ```
2.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🤝 Contributing

We welcome improvements to our map generation process or new styling suggestions! Feel free to open issues or submit pull requests.

## 📄 License

This project is licensed under the [GNU GPL v3.0 License](LICENSE.md).

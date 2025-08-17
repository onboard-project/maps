
import mercantile
import requests
import os
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---

# 1. Tiles type
style = str(input("tiles style: "))

# 2. Bounding box [west, south, east, north]. Get from http://bboxfinder.com/
bbox = [8.934631, 45.328962, 9.725475, 45.722420]  # Example: New York City

# 3. Zoom levels to download (inclusive)
min_zoom = int(input("min zoom: "))
max_zoom = int(input("max zoom: "))
zoom_levels = range(min_zoom, max_zoom + 1)

# 4. Tiles url
tile_url_template = "http://localhost:8080/styles/" + style + "/256/{z}/{x}/{y}.png"
# ---------------------

downloaded_count = 0
total_tiles_to_download = 0


def print_progress_bar():
    global downloaded_count
    global total_tiles_to_download

    percentage = (downloaded_count / total_tiles_to_download) * 100 if total_tiles_to_download > 0 else 0
    bar_length = 50
    filled_length = int(bar_length * percentage // 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {percentage:.2f}% ({downloaded_count}/{total_tiles_to_download})', end='')


def download_tile(url, path):
    global downloaded_count
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        downloaded_count += 1
        print_progress_bar()
        return path
    except requests.exceptions.RequestException as e:
        # We don't increment downloaded_count here as it wasn't successful
        print(f"\nFailed to download {url}: {e}")  # Print on a new line to not interfere with progress bar
        return None


# --- SCRIPT START ---
if __name__ == "__main__":
    all_tiles = []
    for zoom in zoom_levels:
        for tile in mercantile.tiles(bbox[0], bbox[1], bbox[2], bbox[3], zooms=[zoom]):
            all_tiles.append(tile)

    total_tiles_to_download = len(all_tiles)
    print(f"Total tiles to download: {total_tiles_to_download}")

    print_progress_bar()  # Initial progress bar

    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        urls_and_paths = []
        for tile in all_tiles:
            url = tile_url_template.format(z=tile.z, x=tile.x, y=tile.y)
            path = os.path.join("maps\\" + style, str(tile.z), str(tile.x), f"{tile.y}.png")
            urls_and_paths.append((url, path))

        # Map the download function to the URLs and paths
        executor.map(lambda p: download_tile(*p), urls_and_paths)

    print("\n--- Download complete! ---")  # New line after the final progress bar
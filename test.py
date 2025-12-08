import subprocess

def get_now_playing_cli():
    try:
        process = subprocess.run(['nowplaying-cli', 'get', 'title', 'artist', 'album'], capture_output=True, text=True)
        if process.returncode == 0:
            # lines = process.stdout.strip().split('\n')
            # title = lines[0].split(': ')[1] if len(lines) > 0 else "Unknown Title"
            # artist = lines[1].split(': ')[1] if len(lines) > 1 else "Unknown Artist"
            # album = lines[2].split(': ')[1] if len(lines) > 2 else "Unknown Album"
            # return f"{title} by {artist} from {album}"
            return process
        else:
            return "Error retrieving now playing info with nowplaying-cli"
    except FileNotFoundError:
        return "nowplaying-cli not found. Please install it."

print(get_now_playing_cli())
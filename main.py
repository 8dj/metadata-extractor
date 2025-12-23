from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import webbrowser

path = input("image path: ").strip().strip('"')

try:
    img = Image.open(path)

    print(f"\nfile: {path}")
    print(f"size: {img.size[0]}x{img.size[1]}")
    print(f"format: {img.format}\n")

    exif = img._getexif()
    if not exif:
        print("no exif data")
    else:
        for tag_id, value in exif.items():
            name = TAGS.get(tag_id, tag_id)
            print(f"{name}: {value}")

        gps = exif.get(34853)
        if gps:
            print("\n--- gps ---")
            for k, v in gps.items():
                tag = GPSTAGS.get(k, k)
                print(f"{tag}: {v}")

            if 'GPSLatitude' in gps and 'GPSLongitude' in gps:
                def convert(field):
                    return field[0][0]/field[0][1] + field[1][0]/field[1][1]/60 + field[2][0]/field[2][1]/3600

                lat = convert(gps['GPSLatitude'])
                if gps.get('GPSLatitudeRef') == 'S': lat = -lat
                lon = convert(gps['GPSLongitude'])
                if gps.get('GPSLongitudeRef') == 'W': lon = -lon

                print(f"\nlat,lng: {lat:.6f}, {lon:.6f}")
                url = f"https://maps.google.com/?q={lat},{lon}"
                print("opening maps...")
                webbrowser.open(url)

    print("\ndone")

except Exception as e:
    print(f"error: {e}")
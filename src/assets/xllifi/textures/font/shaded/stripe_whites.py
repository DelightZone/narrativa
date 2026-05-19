from PIL import Image
import sys

def process(input_path, output_path="output.png"):
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    WHITE = (255, 255, 255, 255)
    REPLACE = (162, 153, 195, 255)  # #a299c3

    # Pattern: skip 9 rows, replace 3 rows, repeat
    SKIP = 8
    REPLACE_COUNT = 4
    period = SKIP + REPLACE_COUNT  # 12

    for y in range(h):
        if y % period >= SKIP:  # rows 9, 10, 11 in each 12-row cycle
            for x in range(w):
                if pixels[x, y] == WHITE:
                    pixels[x, y] = REPLACE

    img.save(output_path)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stripe_whites.py <input_image> [output_image]")
        sys.exit(1)
    out = sys.argv[2] if len(sys.argv) > 2 else "output.png"
    process(sys.argv[1], out)

import subprocess
import sys
import os

def upscale_and_sharpen(input_video, output_video=None, width=3840, height=2160, crf=18, preset="slow", sharpen="5:5:1.0:5:5:0.0"):
    """
    Upscale video to new resolution and apply sharpening filter using ffmpeg.
    """
    if not os.path.isfile(input_video):
        print(f"Error: File '{input_video}' does not exist.")
        sys.exit(1)

    if not output_video:
        base, ext = os.path.splitext(input_video)
        output_video = f"{base}_upscaled{ext}"

    vf = f"scale={width}:{height},unsharp={sharpen}"

    command = [
        "ffmpeg",
        "-i", input_video,
        "-vf", vf,
        "-c:v", "libx264",
        "-crf", str(crf),
        "-preset", preset,
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        output_video
    ]

    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Error upscaling video:\n", result.stderr.decode())
    else:
        print(f"Video upscaled and sharpened successfully. Output saved to '{output_video}'.")

if __name__ == "__main__":
    # Example usage: python upscale_and_sharpen_video.py input.mp4 output.mp4
    if len(sys.argv) < 2:
        print("Usage: python upscale_and_sharpen_video.py <input_video> [output_video]")
        sys.exit(1)

    input_video = sys.argv[1]
    output_video = sys.argv[2] if len(sys.argv) > 2 else None
    upscale_and_sharpen(input_video, output_video)
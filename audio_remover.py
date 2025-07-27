import subprocess
import sys
import os

def remove_audio(input_video_path, output_video_path=None):
    """
    Removes audio from a video file using ffmpeg, keeping the same video encoding.

    Parameters:
        input_video_path (str): Path to the input video file.
        output_video_path (str, optional): Path to the output video file. If not provided,
                                           appends '_noaudio' before the file extension.

    Returns:
        None
    """
    if not os.path.isfile(input_video_path):
        print(f"Error: File '{input_video_path}' does not exist.")
        sys.exit(1)

    if not output_video_path:
        base, ext = os.path.splitext(input_video_path)
        output_video_path = f"{base}_noaudio{ext}"

    # ffmpeg command: copy video codec, remove audio
    command = [
        "ffmpeg",
        "-i", input_video_path,
        "-c:v", "copy",     # Copy video codec (same encoding)
        "-an",              # Remove audio
        output_video_path
    ]

    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print("Error removing audio:\n", result.stderr.decode())
    else:
        print(f"Audio removed successfully. Output saved to '{output_video_path}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_audio_ffmpeg.py <input_video> [output_video]")
        sys.exit(1)

    input_video = sys.argv[1]
    output_video = sys.argv[2] if len(sys.argv) > 2 else None

    remove_audio(input_video, output_video)
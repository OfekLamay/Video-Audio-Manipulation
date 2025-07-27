import subprocess
import sys
import os

def concat_videos_filter(input_video_paths, output_video_path=None):
    """
    Concatenates multiple videos end-to-end using ffmpeg's filter_complex concat filter.
    This method works even if the input videos have minor differences in encoding parameters.

    Parameters:
        input_video_paths (list of str): List of input video file paths.
        output_video_path (str, optional): Path to the output video file. If not provided,
                                           creates '<first_video>_concat<ext>'.

    Returns:
        None
    """
    if not input_video_paths or len(input_video_paths) < 2:
        print("Error: Please provide at least two video files to concatenate.")
        sys.exit(1)

    for path in input_video_paths:
        if not os.path.isfile(path):
            print(f"Error: File '{path}' does not exist.")
            sys.exit(1)

    first_video = input_video_paths[0]
    base, ext = os.path.splitext(first_video)
    if not output_video_path:
        output_video_path = f"{base}_concat{ext}"

    n = len(input_video_paths)
    inputs = []
    for video in input_video_paths:
        inputs += ["-i", video]

    # Build the filter string for n videos
    filter_parts = []
    for i in range(n):
        filter_parts.append(f'[{i}:v][{i}:a]')
    filter_str = ''.join(filter_parts) + f'concat=n={n}:v=1:a=1[outv][outa]'

    command = [
        "ffmpeg",
        *inputs,
        "-filter_complex", filter_str,
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264",      # Re-encode with H.264 for broad compatibility
        "-c:a", "aac",          # Re-encode with AAC for broad compatibility
        output_video_path
    ]

    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print("Error concatenating videos:\n", result.stderr.decode())
    else:
        print(f"Videos concatenated successfully. Output saved to '{output_video_path}'.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python concat_videos_filter.py <video1> <video2> [video3 ...] [output_video]")
        print("If output_video is not specified, output will be named after the first video with '_concat' suffix.")
        sys.exit(1)

    # Determine if last argument is output filename (has a video extension)
    input_videos = sys.argv[1:-1]
    output_video = sys.argv[-1]
    if not output_video.lower().endswith(('.mp4', '.mov', '.mkv', '.avi')):
        input_videos = sys.argv[1:]
        output_video = None

    concat_videos_filter(input_videos, output_video)
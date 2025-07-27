import subprocess
import sys
import os
import tempfile
import json

def get_video_audio_params(input_video_path):
    """
    Uses ffprobe to retrieve video/audio encoding parameters from the input file.
    Returns a dictionary with relevant parameters.
    """
    ffprobe_cmd = [
        "ffprobe",
        "-v", "error",
        "-show_streams",
        "-show_format",
        "-of", "json",
        input_video_path
    ]
    result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Error running ffprobe:\n", result.stderr.decode())
        sys.exit(1)
    meta = json.loads(result.stdout)
    params = {}
    for stream in meta.get("streams", []):
        if stream["codec_type"] == "video":
            params["v_codec"] = stream.get("codec_name")
            params["v_profile"] = stream.get("profile")
            params["v_pix_fmt"] = stream.get("pix_fmt")
            params["v_width"] = stream.get("width")
            params["v_height"] = stream.get("height")
            params["v_fps"] = eval(stream.get("avg_frame_rate", "0/1"))
            params["v_level"] = stream.get("level", None)
            params["v_bitrate"] = stream.get("bit_rate")
        elif stream["codec_type"] == "audio":
            params["a_codec"] = stream.get("codec_name")
            params["a_sample_rate"] = stream.get("sample_rate")
            params["a_channels"] = stream.get("channels")
            params["a_bitrate"] = stream.get("bit_rate")
    return params

def reverse_video(input_video_path, output_video_path=None):
    """
    Reverses both video and audio of the input video using ffmpeg, matching the original encoding.
    """
    if not os.path.isfile(input_video_path):
        print(f"Error: File '{input_video_path}' does not exist.")
        sys.exit(1)

    if not output_video_path:
        base, ext = os.path.splitext(input_video_path)
        output_video_path = f"{base}_reverse{ext}"

    params = get_video_audio_params(input_video_path)

    # Compose ffmpeg command with matched encoding parameters
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_video_path,
        "-vf", "reverse",
        "-af", "areverse",
        "-c:v", "libx264" if params["v_codec"] == "h264" else params["v_codec"],
        "-profile:v", params["v_profile"].lower() if params.get("v_profile") else "main",
        "-pix_fmt", params["v_pix_fmt"],
        "-r", str(params["v_fps"]),
        "-b:v", f"{int(params['v_bitrate'])//1000}k" if params.get("v_bitrate") else "6000k",
        "-c:a", "aac" if params["a_codec"] == "aac" else params["a_codec"],
        "-ar", str(params["a_sample_rate"]),
        "-ac", str(params["a_channels"]),
        "-b:a", f"{int(params['a_bitrate'])//1000}k" if params.get("a_bitrate") else "160k",
        output_video_path
    ]

    print(f"Running command: {' '.join(ffmpeg_cmd)}")
    result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Error reversing video:\n", result.stderr.decode())
    else:
        print(f"Video reversed successfully. Output saved to '{output_video_path}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reverse_video_matched_encoding.py <input_video> [output_video]")
        sys.exit(1)

    input_video = sys.argv[1]
    output_video = sys.argv[2] if len(sys.argv) > 2 else None

    reverse_video(input_video, output_video)
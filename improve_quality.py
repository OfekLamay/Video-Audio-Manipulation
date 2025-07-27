import subprocess
import sys
import os

def improve_video_quality(input_video_path, output_video_path=None, crf=17, preset='slow', v_bitrate=None, a_bitrate=192, profile='high', level='4.2'):
    """
    Re-encodes a video to improve quality using ffmpeg and libx264.
    You can adjust CRF, preset, video/audio bitrate, profile, and level.

    Parameters:
        input_video_path (str): Path to input video file.
        output_video_path (str, optional): Path to output video file. If not provided, appends '_highq' to filename.
        crf (int): Constant Rate Factor for quality (lower is better, default 17).
        preset (str): x264 encoding preset (default 'slow', options: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow).
        v_bitrate (int, optional): Target video bitrate in kbps. If set, overrides CRF.
        a_bitrate (int): Target audio bitrate in kbps.
        profile (str): H.264 profile (default 'high').
        level (str): H.264 level (default '4.2').
    """
    if not os.path.isfile(input_video_path):
        print(f"Error: File '{input_video_path}' does not exist.")
        sys.exit(1)

    if not output_video_path:
        base, ext = os.path.splitext(input_video_path)
        output_video_path = f"{base}_highq{ext}"

    command = [
        "ffmpeg",
        "-i", input_video_path,
        "-c:v", "libx264",
        "-profile:v", profile,
        "-level:v", level,
        "-preset", preset
    ]

    if v_bitrate:
        command += ["-b:v", f"{v_bitrate}k"]
    else:
        command += ["-crf", str(crf)]

    command += [
        "-c:a", "aac",
        "-b:a", f"{a_bitrate}k",
        "-movflags", "+faststart",  # Better for web playback
        output_video_path
    ]

    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Error improving video quality:\n", result.stderr.decode())
    else:
        print(f"Video processed successfully. Output saved to '{output_video_path}'.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Improve video quality using ffmpeg re-encoding.")
    parser.add_argument("input_video", help="Input video file")
    parser.add_argument("output_video", nargs="?", help="Output video file (optional)")
    parser.add_argument("--crf", type=int, default=17, help="Constant Rate Factor for x264 (lower is better quality)")
    parser.add_argument("--preset", default="slow", help="x264 preset (default: slow)")
    parser.add_argument("--v_bitrate", type=int, help="Video bitrate in kbps (overrides CRF if set)")
    parser.add_argument("--a_bitrate", type=int, default=192, help="Audio bitrate in kbps (default: 192)")
    parser.add_argument("--profile", default="high", help="H.264 profile (default: high)")
    parser.add_argument("--level", default="4.2", help="H.264 level (default: 4.2)")

    args = parser.parse_args()
    improve_video_quality(
        args.input_video,
        args.output_video,
        crf=args.crf,
        preset=args.preset,
        v_bitrate=args.v_bitrate,
        a_bitrate=args.a_bitrate,
        profile=args.profile,
        level=args.level
    )
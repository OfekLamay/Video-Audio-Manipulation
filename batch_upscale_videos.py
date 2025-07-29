import glob
import os
from moviepy import VideoFileClip

def get_resolution(path):
    clip = VideoFileClip(path)
    w, h = clip.size
    clip.close()
    return w, h

def upscale_to_1080p(input_path, output_path):
    clip = VideoFileClip(input_path)
    upscaled = clip.resized(new_size=(1920, 1080))
    upscaled.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="slow"
    )
    clip.close()
    upscaled.close()


def process_videos_in_folder(folder_path, output_folder):
    # Create output folder if not exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Find all common video files
    video_patterns = ['*.mp4', '*.mov', '*.avi', '*.mkv', '*.webm']
    video_files = []
    for pattern in video_patterns:
        video_files.extend(glob.glob(os.path.join(folder_path, pattern)))
    print(f"Found {len(video_files)} video files.")

    for path in video_files:
        print(f"Checking {path}...")
        w, h = get_resolution(path)
        fname = os.path.splitext(os.path.basename(path))[0]
        out_path = os.path.join(output_folder, f"{fname}_1080p.mp4")
        if (w, h) == (1920, 1080):
            print(f"Already 1080p: {path}")
        elif (w, h) == (3840, 2160):
            print(f"Already 2160p (4K): {path} (skipping)")
        else:
            print(f"Upscaling {path} ({w}x{h}) to {out_path} ...")
            upscale_to_1080p(path, out_path)
            print("Done.")


if __name__ == "__main__":
    folder = "videos"  # Your input videos folder
    output_folder = "output_videos"  # Output folder for upscaled videos
    process_videos_in_folder(folder, output_folder)
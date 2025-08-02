from moviepy import VideoFileClip

def upscale_video(input_path, output_path, target_width, target_height):
    """
    Upscales (or resizes) a video to the given dimensions.

    Args:
        input_path (str): Path to the source video file.
        output_path (str): Path to save the upscaled video.
        target_width (int): Target width in pixels.
        target_height (int): Target height in pixels.
    """
    clip = VideoFileClip(input_path)
    upscaled = clip.resized(new_size=(target_width, target_height))
    upscaled.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="slow"
    )
    clip.close()
    upscaled.close()

if __name__ == "__main__":
    # Example usage
    input_video = "vide1.mp4"
    output_video = "output_upscaled.mp4"
    target_width = 1080
    target_height = 1920

    upscale_video(input_video, output_video, target_width, target_height)
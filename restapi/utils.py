import os
import subprocess

def segment_video(video_link, interval_duration):
    """
    Segment video into smaller parts based on interval_duration.
    """
    try:
        output_dir = "segments"
        os.makedirs(output_dir, exist_ok=True)

        # Use FFmpeg to split the video
        cmd = [
            "ffmpeg",
            "-i", video_link,
            "-c", "copy",
            "-map", "0",
            "-segment_time", str(interval_duration),
            "-f", "segment",
            f"{output_dir}/output_%03d.mp4"
        ]
        subprocess.run(cmd, check=True)

        # Return the URLs of the segmented videos
        return [os.path.join(output_dir, f) for f in sorted(os.listdir(output_dir))]
    except Exception:
        return None

def combine_videos(video_links, resolution):
    """
    Combine multiple videos into one with specified resolution.
    """
    try:
        temp_file = "file_list.txt"
        with open(temp_file, "w") as f:
            for link in video_links:
                f.write(f"file '{link}'\n")

        output_file = "combined_video.mp4"

        # Use FFmpeg to combine videos
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", temp_file,
            "-vf", f"scale={resolution['width']}:{resolution['height']}",
            "-c:v", "libx264",
            output_file
        ]
        subprocess.run(cmd, check=True)

        return output_file
    except Exception:
        return None

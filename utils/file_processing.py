import ffmpeg

def compress_video(input_path, output_path, target_size_kb):
    """Compresses a video to a target size using FFmpeg."""
    
    # Calculate the required bitrate to achieve the target size
    probe = ffmpeg.probe(input_path)
    duration = float(probe['format']['duration'])
    total_bitrate_kbps = (target_size_kb * 8) / duration
    video_bitrate_kbps = total_bitrate_kbps * 0.9 # Allocate 90% of bitrate to video

    try:
        ffmpeg.input(input_path) \
            .output(output_path, 
                    vcodec='libx264',  # Use H.264 codec for good compression
                    video_bitrate=f'{video_bitrate_kbps}k', 
                    maxrate=f'{video_bitrate_kbps*1.2}k', # Limit max bitrate
                    bufsize=f'{video_bitrate_kbps*2}k', # Set buffer size
                    acodec='aac',  # Use AAC audio codec
                    audio_bitrate='128k',
                    preset='veryslow', # Optimize for size
                    tune='film', # Optimize for film content
                    crf=23 # Constant Rate Factor (lower value = higher quality, but larger size)
                    ) \
            .run(capture_stdout=True, capture_stderr=True)
        print(f"Video compressed successfully to {output_path}")
    except ffmpeg.Error as e:
        print(f"An error occurred during compression: {e.stderr.decode()}")

# Example usage:
# input_video = 'input_video.mp4'
# output_video = 'output_video.mp4'
# target_size = 1024 # Target size in KB (1MB)
# compress_video(input_video, output_video, target_size)
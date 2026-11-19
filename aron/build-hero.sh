#!/usr/bin/env bash
# Builds the V2 hero film from two clips (e.g. the Dreamina build clip and the walk-in clip).
#
#   ./build-hero.sh build.mp4 inside.mp4
#
# Output, next to v2-video.html:
#   hero-sequence.mp4  both clips joined, no audio, 720p, every frame a keyframe (smooth scroll scrubbing)
#   hero-poster.jpg    first frame, shown before the film decodes
#
# Also useful between the two generations:
#   ./build-hero.sh --last-frame build.mp4    → last-frame.jpg, the start image for the second clip
set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "--last-frame" ]]; then
  ffmpeg -y -loglevel error -sseof -0.1 -i "$2" -frames:v 1 -q:v 2 last-frame.jpg
  echo "last-frame.jpg"; exit 0
fi

[[ $# -eq 2 ]] || { echo "usage: $0 build.mp4 inside.mp4  |  $0 --last-frame clip.mp4"; exit 1; }

# Join at 24 fps and 1280x720 whatever the clips' native size, then encode all-intra.
ffmpeg -y -loglevel error -i "$1" -i "$2" -filter_complex \
  "[0:v]fps=24,scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1[a];\
   [1:v]fps=24,scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1[b];\
   [a][b]concat=n=2:v=1:a=0[v]" \
  -map "[v]" -an -c:v libx264 -g 1 -keyint_min 1 -sc_threshold 0 -crf 22 -preset medium \
  -pix_fmt yuv420p -movflags +faststart hero-sequence.mp4

ffmpeg -y -loglevel error -i hero-sequence.mp4 -frames:v 1 -q:v 3 hero-poster.jpg
ls -lh hero-sequence.mp4 hero-poster.jpg

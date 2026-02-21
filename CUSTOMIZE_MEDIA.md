# 🎵 How to Customize Music & Videos

## Overview

ZenStressy now includes **music and video recommendations** that adapt to your stress level! You can easily customize these to add your own favorite tracks and videos.

## Media Structure by Stress Level

### 🟢 LOW STRESS
**Music**: Peaceful, uplifting, ambient
**Videos**: Motivational, inspirational, success stories

### 🟡 MEDIUM STRESS  
**Music**: Calming, meditation, piano relaxation
**Videos**: Breathing guides, stress management, self-help

### 🔴 HIGH STRESS
**Music**: Emergency calm, anxiety relief, healing frequencies
**Videos**: Crisis management, immediate calm techniques, panic guides

## How to Add Your Own Media

### Step 1: Get YouTube Video IDs

1. Find your favorite YouTube video
2. Copy the video URL
3. Extract the **video ID** (the part after `v=`)

**Example:**
```
https://www.youtube.com/watch?v=jfKfPfyJRdk
                                  ^^^^^^^^^^^
                            This is the video ID
```

### Step 2: Update app.py

Open `app.py` and find the `get_stress_media()` function (around line 121).

Look for the section you want to customize:

```python
'Low': {
    'songs': [
        {'title': 'Peaceful Morning', 
         'url': 'https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=0', 
         'type': 'ambient'},
        # Add your music here!
    ],
    'videos': [
        {'title': 'Motivation for Success', 
         'url': 'https://www.youtube.com/embed/ZXsQAXx_ao0?autoplay=0', 
         'type': 'motivational'},
        # Add your videos here!
    ]
}
```

### Step 3: Add Your Content

Replace or add media items using this format:

```python
{'title': 'Your Song/Video Title', 
 'url': 'https://www.youtube.com/embed/YOUR_VIDEO_ID?autoplay=0', 
 'type': 'category'}
```

**Important:** 
- Use **YouTube embed URL**: `https://www.youtube.com/embed/VIDEO_ID`
- Add `?autoplay=0` at the end to prevent auto-play
- Replace `VIDEO_ID` with your actual video ID

### Step 4: Choose Categories

Use descriptive types for your media:
- **Music**: ambient, nature, uplifting, meditation, piano, soothing, sleep, emergency, instant, anxiety, healing, therapy
- **Videos**: motivational, inspirational, self-help, breathing, uplifting, crisis, immediate, panic, healing

## Complete Examples

### Adding Music for Low Stress

```python
'Low': {
    'songs': [
        {'title': 'Peaceful Morning', 
         'url': 'https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=0', 
         'type': 'ambient'},
        {'title': 'Your Favorite Song',           # Your title
         'url': 'https://www.youtube.com/embed/ABC123XYZ?autoplay=0',  # Your video ID
         'type': 'uplifting'},                    # Category
        {'title': 'Another Great Track',
         'url': 'https://www.youtube.com/embed/DEF456UVW?autoplay=0',
         'type': 'nature'}
    ],
}
```

### Adding Videos for High Stress

```python
'High': {
    'videos': [
        {'title': 'Crisis Stress Management', 
         'url': 'https://www.youtube.com/embed/gkQpPov6anE?autoplay=0', 
         'type': 'crisis'},
        {'title': 'Your Comfort Video',           # Your title
         'url': 'https://www.youtube.com/embed/GHI789RST?autoplay=0',  # Your video ID
         'type': 'immediate'},                    # Category
        {'title': 'Encouraging Message',
         'url': 'https://www.youtube.com/embed/JKL012NOP?autoplay=0',
         'type': 'healing'}
    ]
}
```

## Quick Reference

### Embed URL Format
```
https://www.youtube.com/embed/VIDEO_ID?autoplay=0
```

### Regular YouTube URL vs Embed URL
```
Regular:  https://www.youtube.com/watch?v=jfKfPfyJRdk
Embed:    https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=0
```

### Where to Put Media
```python
# In app.py, function get_stress_media()

'Low': {      # For low stress level
    'songs': [ ... ],    # Add songs here
    'videos': [ ... ]    # Add videos here
},
'Medium': {   # For medium stress level
    'songs': [ ... ],
    'videos': [ ... ]
},
'High': {     # For high stress level
    'songs': [ ... ],
    'videos': [ ... ]
}
```

## Tips for Best Experience

### Music Selection
✅ **Low Stress**: Upbeat, happy, energetic music
✅ **Medium Stress**: Calming, slow-tempo, instrumental
✅ **High Stress**: Very calm, minimal, frequencies (432Hz, 528Hz)

### Video Selection
✅ **Low Stress**: Success stories, motivation, goal-setting
✅ **Medium Stress**: Breathing exercises, meditation guides, tips
✅ **High Stress**: Immediate relief techniques, crisis support, calming visuals

### Technical Tips
- Keep titles under 40 characters for best display
- Use descriptive, meaningful types
- Test each link before adding
- Add 3-5 items per category for variety
- Mix different content creators/styles

## Testing Your Changes

1. **Save** `app.py` after making changes
2. **Restart** the server: `python app.py`
3. **Go to** dashboard
4. **Predict** stress level
5. **Check** media section appears
6. **Click** play on your custom media!

## Example: Full Custom Setup

```python
def get_stress_media(stress_level):
    """Get music and video recommendations based on stress level"""
    media = {
        'Low': {
            'songs': [
                {'title': 'Morning Energy Boost', 
                 'url': 'https://www.youtube.com/embed/YOUR_ID_HERE?autoplay=0', 
                 'type': 'uplifting'},
                {'title': 'Success Music', 
                 'url': 'https://www.youtube.com/embed/YOUR_ID_HERE?autoplay=0', 
                 'type': 'motivational'},
            ],
            'videos': [
                {'title': 'Achieve Your Dreams', 
                 'url': 'https://www.youtube.com/embed/YOUR_ID_HERE?autoplay=0', 
                 'type': 'motivational'},
            ]
        },
        'Medium': {
            'songs': [
                {'title': 'Relaxing Piano', 
                 'url': 'https://www.youtube.com/embed/YOUR_ID_HERE?autoplay=0', 
                 'type': 'piano'},
                {'title': 'Meditation Sounds', 
                 'url': 'https://www.youtube.com/embed/YOUR_ID_HERE?autoplay=0', 
                 'type': 'meditation'},
            ],
            'videos': [
                {'title': 'Calm Your Mind', 
                 'url': 'https://www.youtube.com/embed/YOUR_ID_HERE?autoplay=0', 
                 'type': 'breathing'},
            ]
        },
        'High': {
            'songs': [
                {'title': 'Instant Relief Music', 
                 'url': 'https://www.youtube.com/embed/YOUR_ID_HERE?autoplay=0', 
                 'type': 'instant'},
                {'title': 'Healing Frequencies', 
                 'url': 'https://www.youtube.com/embed/YOUR_ID_HERE?autoplay=0', 
                 'type': 'healing'},
            ],
            'videos': [
                {'title': 'Immediate Calm Guide', 
                 'url': 'https://www.youtube.com/embed/YOUR_ID_HERE?autoplay=0', 
                 'type': 'immediate'},
            ]
        }
    }
    return media.get(stress_level, {'songs': [], 'videos': []})
```

**Replace `YOUR_ID_HERE` with actual YouTube video IDs!**

## Need Help?

- **Video not loading**: Check that you're using embed URL format
- **Autoplay issues**: Make sure `?autoplay=0` is at the end
- **Not showing**: Restart the server after changes
- **Display issues**: Check browser console for errors

## Current Default Media

The app comes with **curated YouTube videos** by default:
- **Low**: 3 songs, 2 videos
- **Medium**: 4 songs, 3 videos  
- **High**: 5 songs, 4 videos

You can keep these or replace them all with your favorites!

---

**Enjoy your personalized stress relief experience! 🎵📹**


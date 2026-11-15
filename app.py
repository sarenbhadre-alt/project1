
import streamlit as st
import json
import urllib.parse
import urllib.request
from dotenv import load_dotenv
from google import genai
from google.genai import types

# LOAD GEMINI API
load_dotenv()
client = genai.Client()

# PAGE SETTINGS
st.set_page_config(
    page_title="MOODSCAPE",
    page_icon="🎧",
    layout="wide"
)

# DREAMY DESIGN
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #0b0618,
        #1c1035,
        #111827
    );
    color: #f0eaff;
}

h1, h2, h3 {
    color: #e5d5ff !important;
}

p, label {
    color: #d5c9ed !important;
}

.stButton > button {
    background: linear-gradient(90deg, #8b5cf6, #6366f1);
    color: white;
    border-radius: 15px;
    border: none;
    padding: 12px 25px;
}

.stButton > button:hover {
    background: #a78bfa;
    color: white;
}

div[data-testid="stForm"] {
    background: rgba(255,255,255,0.04);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# HOMEPAGE
st.markdown(
    "<h1 style='text-align:center;'>MOODSCAPE ✦</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>"
    "Your emotions. Your sound. Your universe."
    "</p>",
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown("## ✧ Let's create your personal soundscape")

st.write(
    "Tell us about your mood, your music taste, "
    "and the artists you love. We'll create a playlist "
    "that feels like YOU."
)

# USER QUESTIONNAIRE
with st.form("music_preferences"):

    st.markdown("### 🌙 What are you feeling?")

    mood = st.selectbox(
        "Choose your current mood",
        [
            "Dreamy and weightless",
            "Melancholic and emotional",
            "Peaceful and calm",
            "Nostalgic",
            "Happy and energetic",
            "Lonely and detached",
            "Romantic",
            "Angry and intense",
            "Something else"
        ]
    )

    if mood == "Something else":
        custom_mood = st.text_input("Describe your mood")
    else:
        custom_mood = ""

    st.markdown("### 🎵 What kind of music do you enjoy?")

    genres = st.multiselect(
        "Select your preferred genres",
        [
            "Dream Pop", "Alternative", "Indie", "R&B",
            "Pop", "Rock", "Hip-Hop", "Psychedelic",
            "Lo-fi", "Electronic", "Ambient", "Soul",
            "Classical", "Other"
        ]
    )

    music_style = st.text_input(
        "Describe the sound you want",
        placeholder="e.g. hazy, atmospheric, slow, immersive..."
    )

    st.markdown("### 🎤 Your favourite artists")

    artists_input = st.text_input(
        "Enter 3 to 5 artists, separated by commas",
        placeholder="e.g. Joji, Radiohead, Deftones, Oasis"
    )

    st.markdown("### 🌍 Language preference")

    language = st.selectbox(
        "Which language should your playlist use?",
        [
            "English", "Hindi", "Kannada", "Tamil",
            "Telugu", "Malayalam", "Spanish", "Korean",
            "Japanese", "French", "Any language", "Other"
        ]
    )

    st.markdown("### ⏳ Playlist duration")

    duration = st.slider(
        "How long should your playlist be?",
        min_value=15,
        max_value=180,
        value=60,
        step=15,
        format="%d minutes"
    )

    st.markdown("### ✨ Personalisation")

    customisation = st.text_area(
        "Anything else you'd like?",
        placeholder="e.g. Avoid loud songs, include underrated tracks, make it feel cinematic..."
    )

    save_playlist = st.checkbox("I want to save my playlist")

    submitted = st.form_submit_button("✦ Create My Soundscape")

# GENERATE PLAYLIST
if submitted:

    artists = [
        artist.strip()
        for artist in artists_input.split(",")
        if artist.strip()
    ]

    if len(artists) < 3 or len(artists) > 5:
        st.error("Please enter between 3 and 5 artists.")

    elif not genres:
        st.error("Please select at least one music genre.")

    elif mood == "Something else" and not custom_mood.strip():
        st.error("Please describe your mood.")

    else:

        final_mood = custom_mood if mood == "Something else" else mood

        number_of_songs = round(duration / 3.5)

        

        prompt = f"""
You are MOODSCAPE, an intelligent music curator.

Your job is to create a carefully curated playlist that
feels like a continuous musical experience.

USER PREFERENCES:

Mood: {final_mood}
Genres: {", ".join(genres)}
Favourite artists: {", ".join(artists)}
Language: {language}
Duration: {duration} minutes
Desired sound: {music_style}
Additional preferences: {customisation}

PLAYLIST RULES:

1. Recommend approximately {number_of_songs} songs.

2. Recommend only real, officially released songs.
Never invent titles, artists or collaborations.

3. Verify that every song belongs to the correct artist.
Do not guess song credits.

4. Maintain artist diversity.
Ideally, recommend no more than 2 songs per artist.
Never allow one artist to dominate the playlist.

5. Include favourite artists, but also discover artists
with similar musical qualities.

6. Avoid unnecessary repetition and generic recommendations.

7. Every song explanation must describe specific,
recognisable musical characteristics of that track.
Do not repeatedly use words like dreamy, hazy and
atmospheric without explaining why the song fits.

8. Respect the user's mood, genres and preferences.
Do not introduce songs that disrupt the intended mood.

MUSICAL JOURNEY:

Divide the playlist into three phases:

- The Opening: Introduce the mood gently.
- The Drift: Explore the deeper emotional and musical
  atmosphere.
- The Arrival: End with a satisfying, memorable finish.

The transitions between phases should feel natural.

Return ONLY valid JSON in this exact structure:

{{
    "playlist_name": "Creative playlist name",
    "description": "Short playlist description",
    "songs": [
        {{
            "title": "Song title",
            "artist": "Artist name",
            "reason": "Specific explanation of why this song fits",
            "phase": "The Opening"
        }}
    ],
    "listening_experience": "Closing description"
}}

Use only these phase names:
The Opening, The Drift, The Arrival.

Return approximately {number_of_songs} songs.
"""


        st.markdown("---")
        st.markdown("## ✧ Your Personal Soundscape")

        try:
            with st.spinner("Creating your musical universe... 🎧"):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )

            playlist = json.loads(response.text)

            st.markdown(f"# 🎧 {playlist['playlist_name']}")
            st.write(playlist["description"])

            st.markdown("---")
            st.markdown("### ✦ Your Tracks")

            current_phase = None
            for i, song in enumerate(playlist["songs"], start=1):
                      current_phase = None

            for i, song in enumerate(playlist["songs"], start=1):

                phase = song.get("phase", "The Drift")

                if phase != current_phase:
                    st.markdown(f"### ✧ {phase}")
                    current_phase = phase

                title = song["title"]
                artist = song["artist"]

                # Create a Spotify search link
                search_query = urllib.parse.quote(
                    f"{title} {artist}"
                )
                spotify_link = (
                    f"https://open.spotify.com/search/{search_query}"
                )

                # Find album artwork
                image_url = None

                try:
                    search_url = (
                        "https://itunes.apple.com/search?"
                        + urllib.parse.urlencode({
                            "term": f"{title} {artist}",
                            "entity": "song",
                            "limit": 1
                        })
                    )

                    with urllib.request.urlopen(
                        search_url, timeout=5
                    ) as result:
                        data = json.loads(result.read().decode())

                    if data.get("results"):
                        image_url = data["results"][0].get(
                            "artworkUrl100"
                        )

                except Exception:
                    image_url = None

                # DISPLAY THE SONG CARD
                with st.container(border=True):

                    col1, col2 = st.columns([1, 3])

                    with col1:
                        if image_url:
                            st.image(image_url, use_container_width=True)
                        else:
                            st.markdown("🎵")

                    with col2:
                        st.markdown(
                            f"### {i:02d}. {title}"
                        )

                        st.write(f"**{artist}**")

                        st.caption(
                            f"✧ {song['reason']}"
                        )

                        st.markdown(
                            f"[♫ Find on Spotify]({spotify_link})"
                        )

            st.markdown("---")
            st.markdown("### 🌙 The Listening Experience")

            st.write(playlist["listening_experience"])

            st.success("Your soundscape has been generated!")

            st.caption(
                "Recommendations are AI-generated. "
                "Please verify song details before adding "
                "them to your music library."
            )

        except json.JSONDecodeError:
            st.error(
                "The AI returned an unexpected format. "
                "Please try generating your playlist again."
            )

        except Exception as e:
            st.error(
                "Something went wrong while generating your playlist."
            )
            st.caption(f"Technical details: {e}")

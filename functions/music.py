import time
import musicalbeeps

# use musicalbeeps to play a sound without blocking the GUI
def play_sound():
    
    # Define the notes and duration for the melody
    note_duration = 0.2
    melody = ["C#", "D", "E", "F#", "G", "A", "B", "C#"]
    verse1_notes = ["C#", "D", "E", "F#", "G", "A", "B", "C#"]
    chorus1_notes = ["C#", "G#", "F#", "G#", "A#", "B", "C#", "G#"]
    verse2_notes = ["D#", "E", "F#", "G#", "A", "B", "C#", "D#"]
    bridge_notes = ["G#", "D#", "C#", "G#", "B", "A", "G#", "F#"]
    chorus2_notes = ["C#", "G#", "F#", "G#", "A#", "B", "C#", "G#"]

    # Create a new player
    player = musicalbeeps.Player(volume=0.1, mute_output=True)

    # Play the melody for 8 bars
    for i in range(4):
        for note in melody:
            player.play_note(note, note_duration)

    # First verse
    for i in range(2):
        for note in verse1_notes:
            player.play_note(note, note_duration)

    # First chorus
    for i in range(2):
        for note in chorus1_notes:
            player.play_note(note, note_duration)

    # Second verse
    for i in range(2):
        for note in verse2_notes:
            player.play_note(note, note_duration)

    # Bridge
    for i in range(2):
        for note in bridge_notes:
            player.play_note(note, note_duration)

    # Second chorus
    for i in range(2):
        for note in chorus2_notes:
            player.play_note(note, note_duration)

    # Repeat the melody for 8 bars
    for i in range(8):
        for note in melody:
            player.play_note(note, note_duration)

    # Repeat the song for 1 minute
    for i in range(3):
        # First verse
        for i in range(2):
            for note in verse1_notes:
                player.play_note(note, note_duration)

        # First chorus
        for i in range(2):
            for note in chorus1_notes:
                player.play_note(note, note_duration)

        # Second verse
        for i in range(2):
            for note in verse2_notes:
                player.play_note(note, note_duration)

        # Bridge
        for i in range(2):
            for note in bridge_notes:
                player.play_note(note, note_duration)

        # Second chorus
        for i in range(2):
            for note in chorus2_notes:
                player.play_note(note, note_duration)

        # Repeat the melody for 8 bars
        for i in range(8):
            for note in melody:
                player.play_note(note, note_duration)

    # Wait for the song to finish
    time.sleep(2)

    # Stop the player
    player.stop()
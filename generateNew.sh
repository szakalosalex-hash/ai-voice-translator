#!/bin/bash

# --- CONFIG ---
API_KEY="sk_50f0a34101e066a155ec55d6b34a2e0119e3770384bb2fb3"
VOICE_ID="21m00Tcm4TlvDq8ikWAM"
MODEL="eleven_multilingual_v2"

# --- 1. INPUT VALIDATION ---
INPUT_FILE="$1"
if [ ! -f "$INPUT_FILE" ]; then echo "File not found"; exit 1; fi

# --- 2. INTERACTIVE LANGUAGE SELECTION ---
echo "--------------------------------------"
echo "  ELEVENLABS TRANSLATOR TOOL"
echo "--------------------------------------"
echo "Common codes: es (Spanish), fr (French), de (German), it (Italian), ja (Japanese)"
echo -n "Enter target language code: "
read TARGET_LANG

# Fallback if you just hit enter
if [ -z "$TARGET_LANG" ]; then TARGET_LANG="es"; fi

# --- 3. TRANSLATION ---
echo "Translating to [$TARGET_LANG]..."
ORIGINAL_TEXT=$(cat "$INPUT_FILE")
TRANSLATED_TEXT=$(python -m translate -t "$TARGET_LANG" "$ORIGINAL_TEXT")

TEMP_FILE="temp_translated.txt"
echo "$TRANSLATED_TEXT" > "$TEMP_FILE"

# --- 4. SMART FILENAME ---
BASE_NAME="${INPUT_FILE%.*}"
OUTPUT_FILE="$BASE_NAME ($TARGET_LANG).mp3"

counter=1
while [ -f "$OUTPUT_FILE" ]; do
    OUTPUT_FILE="$BASE_NAME ($TARGET_LANG) ($counter).mp3"
    ((counter++))
done

# --- 5. EXECUTION ---
python -m httpie POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID" \
    xi-api-key:"$API_KEY" \
    text=@"$TEMP_FILE" \
    model_id="$MODEL" \
    --output "$OUTPUT_FILE"

# Cleanup
rm "$TEMP_FILE"

if [ $? -eq 0 ]; then
    echo "Done! Created $OUTPUT_FILE"
    powershell.exe -c "(New-Object Media.SoundPlayer 'C:\Windows\Media\notify.wav').PlaySync()"
    sleep 3
fi
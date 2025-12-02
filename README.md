# 🎥 Movie Mode Light Control
## Turn Off Lights Automatically During Movies!

**Movie Mode Light Control**, designed to help automate your movie nights by dimming the environment when your movie starts — and bringing everything back to life when you pause or stop.

### 🎥 What It Does

This blueprint detects when your media player (e.g., TV or streaming device) starts playing and:

* **Sends a notification** asking if you want to activate Movie Mode.
* **Turns off selected lights or switches** automatically when Movie Mode is enabled.
* **Restores your previous light/switch states** when the movie is paused or stopped.
* **Automatically disables Movie Mode** when the media ends or stops.
* **Only activates after a specific time** (e.g., after 9:00 PM) to avoid triggering during the day.

---

### 🧠 How It Works

It uses a combination of:

* `media_player` state triggers (Playing, Paused, Idle, etc.)
* An `input_boolean` helper to track Movie Mode status.
* Optional `notify` service to ask for user confirmation (e.g., via mobile app).
* Customizable activation time.

You can also customize:

* Notification target (e.g., `mobile_app_yourphone`)
* Notification title & message
* Trigger states for play, pause, and off
* Lights/switches to be controlled

---

### 🧩 Inputs Required

* Media Player Entity (e.g., your TV or streaming stick)
* Trigger states (playing, paused, idle, etc.)
* Movie Mode Helper (input_boolean)
* Notification Target (optional)
* Lights/Switches to control
* Activation time (e.g., 21:00)

---

### 🚀 How to Use

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](upload://3IEiMyDuriGlhMmaFV0iSnXlL0b)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmuratcesmecioglu%2Fha-movie-mode%2Fblob%2Fmain%movie-mode.yaml)
[Github](https://github.com/muratcesmecioglu/ha-movie-mode)

1. Add this blueprint
2. Fill in the fields with your media player, lights, and notification settings.
3. Enjoy hands-free ambience for your movie nights!

---

## 🧪 Validate the blueprint locally

An MVP validator is included to generate a throwaway Home Assistant configuration and optionally run `hass --script check_config` against it.

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Generate the validation bundle (creates `.ha-validator/` with a demo config and copies the blueprint):

   ```bash
   python validator.py movie-mode.yaml
   ```

3. If you have Home Assistant installed locally, run the built-in config check:

   ```bash
   python validator.py movie-mode.yaml --run-check-config
   ```

   The script will report whether `hass --script check_config` succeeded and surface any schema issues it found.

### 🐳 Validate using Docker (includes Home Assistant)

If you do not have Home Assistant installed locally, you can run the validator inside a container that bundles all dependencies:

```bash
# Build the validator image
docker build -t ha-movie-mode-validator .

# Run the validation with hass --script check_config
docker run --rm ha-movie-mode-validator

# To keep the generated .ha-validator directory, mount the repo as a volume
docker run --rm -v "$PWD":/app ha-movie-mode-validator
```

The default container command mirrors `python validator.py movie-mode.yaml --run-check-config` and will exit non-zero if the config check fails.

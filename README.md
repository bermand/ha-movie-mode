# 🎥 Movie Mode Light Control
## Apply a Movie Scene Automatically During Movies!

**Movie Mode Light Control**, designed to help automate your movie nights by activating a custom scene when your movie starts — and bringing everything back to its prior state when you pause or stop.

### 🎥 What It Does

This blueprint detects when your media player (e.g., TV or streaming device) starts playing and:

* **Activates a chosen scene** automatically when Movie Mode is enabled.
* **Captures and restores your previous light/switch states** when the movie is paused or stopped.
* **Automatically disables Movie Mode** when the media ends or stops.
* **Only activates after a specific time** (e.g., after 9:00 PM) to avoid triggering during the day.

---

### 🧠 How It Works

It uses a combination of:

* `media_player` state triggers (Playing, Paused, Idle, etc.)
* An `input_boolean` helper to track Movie Mode status.
* Customizable activation time.

You can also customize:

* Trigger states for play, pause, and off
* Lights/switches to be controlled
* Scene to apply while in Movie Mode

---

### 🧩 Inputs Required

* Media Player Entity (e.g., your TV or streaming stick)
* Trigger states (playing, paused, idle, etc.)
* Movie Mode Helper (input_boolean)
* Lights/Switches to control
* Scene to activate during Movie Mode
* Activation time (e.g., 21:00)

---

### 🚀 How to Use

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](upload://3IEiMyDuriGlhMmaFV0iSnXlL0b)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmuratcesmecioglu%2Fha-movie-mode%2Fblob%2Fmain%movie-mode.yaml)
[Github](https://github.com/muratcesmecioglu/ha-movie-mode)

1. Add this blueprint
2. Fill in the fields with your media player, lights, and scene settings.
3. Enjoy hands-free ambience for your movie nights!

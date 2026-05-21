import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw
import numpy as np
import pygame
import wave

SAMPLE_RATE = 44100
NOTE_DURATION = 0.5
WIDTH = 80

SCALE = [
    261.63, 293.66, 329.63, 349.23,
    392.00, 440.00, 493.88, 523.25
]


def brightness_to_frequency(brightness):
    index = int(((255-brightness) / 255) * (len(SCALE) - 1))
    return SCALE[index]



def make_tone(freq, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave_data = np.sin(2 * np.pi * freq * t)

    fade_len = min(500, len(wave_data) // 2)
    wave_data[:fade_len] *= np.linspace(0, 1, fade_len)
    wave_data[-fade_len:] *= np.linspace(1, 0, fade_len)

    return wave_data


def image_to_sound(img):
    img = img.convert("L")

    aspect = img.height / img.width
    new_height = max(8, int(WIDTH * aspect))
    img = img.resize((WIDTH, new_height))

    pixels = np.array(img)
    audio = []

    for x in range(pixels.shape[1]):
        column = pixels[:, x]
        avg_brightness = np.mean(column)

        freq = brightness_to_frequency(avg_brightness)
        tone = make_tone(freq, NOTE_DURATION)
        audio.append(tone)

    audio = np.concatenate(audio)

    max_value = np.max(np.abs(audio))
    if max_value > 0:
        audio = audio / max_value

    return (audio * 32767).astype(np.int16)


def save_wav(filename, audio):
    with wave.open(filename, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio.tobytes())


class DrawingMusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw to Music")
        self.root.geometry("850x750")
        self.root.configure(bg="#121212")

        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)

        self.audio = None
        self.is_playing = False
        self.visualizer_job = None

        self.last_x = None
        self.last_y = None

        self.canvas_width = 560
        self.canvas_height = 330

        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        title = tk.Label(
            root,
            text="🎨 Draw to Music 🎵",
            font=("Arial", 28, "bold"),
            bg="#121212",
            fg="#ffffff"
        )
        title.pack(pady=15)

        subtitle = tk.Label(
            root,
            text="Draw something, convert it into notes, then watch the sound wave.",
            font=("Arial", 12),
            bg="#121212",
            fg="#bbbbbb"
        )
        subtitle.pack(pady=3)

        self.canvas_frame = tk.Frame(root, bg="#2a2a2a", padx=8, pady=8)
        self.canvas_frame.pack(pady=15)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        self.wave_label = tk.Label(
            root,
            text="Sound Wave Visualizer",
            font=("Arial", 14, "bold"),
            bg="#121212",
            fg="#ffffff"
        )
        self.wave_label.pack(pady=(10, 4))

        self.wave_canvas = tk.Canvas(
            root,
            width=700,
            height=130,
            bg="#050505",
            highlightthickness=1,
            highlightbackground="#333333"
        )
        self.wave_canvas.pack(pady=5)

        self.button_frame = tk.Frame(root, bg="#121212")
        self.button_frame.pack(pady=15)

        self.convert_button = tk.Button(
            self.button_frame,
            text="Convert",
            font=("Arial", 13, "bold"),
            width=14,
            bg="#4caf50",
            fg="white",
            activebackground="#66bb6a",
            command=self.convert_drawing
        )
        self.convert_button.grid(row=0, column=0, padx=8)

        self.play_button = tk.Button(
            self.button_frame,
            text="Play",
            font=("Arial", 13, "bold"),
            width=14,
            bg="#2196f3",
            fg="white",
            activebackground="#42a5f5",
            command=self.play_music
        )
        self.play_button.grid(row=0, column=1, padx=8)

        self.save_button = tk.Button(
            self.button_frame,
            text="Save WAV",
            font=("Arial", 13, "bold"),
            width=14,
            bg="#9c27b0",
            fg="white",
            activebackground="#ab47bc",
            command=self.save_music
        )
        self.save_button.grid(row=0, column=2, padx=8)

        self.reset_button = tk.Button(
            self.button_frame,
            text="Reset",
            font=("Arial", 13, "bold"),
            width=14,
            bg="#f44336",
            fg="white",
            activebackground="#ef5350",
            command=self.reset_canvas
        )
        self.reset_button.grid(row=0, column=3, padx=8)

        self.status = tk.Label(
            root,
            text="Draw something on the canvas.",
            font=("Arial", 12),
            bg="#121212",
            fg="#dddddd"
        )
        self.status.pack(pady=10)

        self.draw_empty_wave()

    def start_draw(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def stop_draw(self, event):
        self.last_x = None
        self.last_y = None

    def draw_line(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                fill="black",
                width=7,
                capstyle=tk.ROUND,
                smooth=True
            )

            self.draw.line(
                [self.last_x, self.last_y, event.x, event.y],
                fill="black",
                width=7
            )

        self.last_x = event.x
        self.last_y = event.y

    def convert_drawing(self):
        self.status.config(text="Converting drawing into music...")
        self.root.update()

        self.audio = image_to_sound(self.image)

        self.draw_waveform(self.audio)
        self.status.config(text="Converted! Press Play to hear it.")

    def play_music(self):
        if self.audio is None:
            messagebox.showwarning("No Music", "Please convert your drawing first.")
            return

        pygame.mixer.stop()

        audio = self.audio.astype(np.int16)

        if len(audio.shape) == 1:
            audio = np.column_stack((audio, audio))

        sound = pygame.sndarray.make_sound(audio)
        sound.play()

        self.is_playing = True
        self.status.config(text="Playing music...")
        self.animate_waveform()

    def save_music(self):
        if self.audio is None:
            messagebox.showwarning("No Music", "Please convert your drawing first.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV File", "*.wav")]
        )

        if path:
            save_wav(path, self.audio)
            self.status.config(text="Music saved as WAV!")

    def reset_canvas(self):
        pygame.mixer.stop()

        if self.visualizer_job is not None:
            self.root.after_cancel(self.visualizer_job)
            self.visualizer_job = None

        self.canvas.delete("all")
        self.wave_canvas.delete("all")

        self.image = Image.new(
            "RGB",
            (self.canvas_width, self.canvas_height),
            "white"
        )
        self.draw = ImageDraw.Draw(self.image)

        self.audio = None
        self.is_playing = False
        self.last_x = None
        self.last_y = None

        self.draw_empty_wave()
        self.status.config(text="Canvas reset. Draw something new.")

    def draw_empty_wave(self):
        self.wave_canvas.delete("all")

        w = int(self.wave_canvas["width"])
        h = int(self.wave_canvas["height"])
        mid = h // 2

        self.wave_canvas.create_line(
            20,
            mid,
            w - 20,
            mid,
            fill="#333333",
            width=2
        )

        self.wave_canvas.create_text(
            w // 2,
            mid - 20,
            text="Convert your drawing to see the waveform",
            fill="#777777",
            font=("Arial", 11)
        )

    def draw_waveform(self, audio, playhead_x=None):
        self.wave_canvas.delete("all")

        w = int(self.wave_canvas["width"])
        h = int(self.wave_canvas["height"])
        mid = h // 2

        self.wave_canvas.create_line(
            0,
            mid,
            w,
            mid,
            fill="#222222",
            width=1
        )

        if audio is None or len(audio) == 0:
            return

        samples = audio.astype(np.float32) / 32767.0

        step = max(1, len(samples) // w)
        points = []

        for x in range(w):
            idx = x * step
            if idx < len(samples):
                y = mid - samples[idx] * (h * 0.42)
                points.append((x, y))

        for i in range(len(points) - 1):
            self.wave_canvas.create_line(
                points[i][0],
                points[i][1],
                points[i + 1][0],
                points[i + 1][1],
                fill="#00e5ff",
                width=2
            )

        if playhead_x is not None:
            self.wave_canvas.create_line(
                playhead_x,
                0,
                playhead_x,
                h,
                fill="#ffeb3b",
                width=3
            )

    def animate_waveform(self):
        if self.audio is None:
            return

        length_seconds = len(self.audio) / SAMPLE_RATE
        start_time = pygame.time.get_ticks()

        def update():
            elapsed = (pygame.time.get_ticks() - start_time) / 1000

            if elapsed >= length_seconds:
                self.draw_waveform(self.audio)
                self.status.config(text="Finished playing.")
                self.is_playing = False
                return

            w = int(self.wave_canvas["width"])
            playhead_x = int((elapsed / length_seconds) * w)

            self.draw_waveform(self.audio, playhead_x)
            self.visualizer_job = self.root.after(40, update)

        update()


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingMusicApp(root)
    root.mainloop()
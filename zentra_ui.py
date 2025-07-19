import tkinter as tk

class ZentraUI:
    """Manages the floating UI component for Zentra."""
    def __init__(self, root):
        self.root = root
        self.is_running = True  # Flag to control the animation loop
        self.root.title("Zentra")
        
        self.root.overrideredirect(True)
        self.root.geometry("+50+50")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "black")
        
        self.animation_frames = ["( Z.z )", "( o.o )", "( ^.^ )", "( o.o )"]
        self.frame_index = 0
        
        self.label = tk.Label(
            self.root, 
            text=self.animation_frames[0], 
            font=("Consolas", 20, "bold"), 
            bg="black",
            fg="#00ff99"
        )
        self.label.pack(padx=10, pady=5)
        self.animate()

    def animate(self):
        """Cycles through the frames to create animation."""
        # Only update and schedule the next frame if the UI is running
        if self.is_running:
            self.label.config(text=self.animation_frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            self.root.after(700, self.animate)

    def stop(self):
        """Stops the animation loop gracefully."""
        self.is_running = False
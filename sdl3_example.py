from ctypes import c_char_p, c_int, c_uint32, c_float, byref, POINTER
import sdl3

class SDL3ExampleApp:
    height: int
    width: int
    title: str

    window: sdl3.LP_SDL_Window
    renderer: sdl3.LP_SDL_Renderer

    # Initialize the window, renderers, etc.
    def __init__(self) -> None:
        if not sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO | sdl3.SDL_INIT_EVENTS): # pyright: ignore [reportArgumentType]
            raise RuntimeError(f"SDL_Init failed: {sdl3.SDL_GetError()}")

        self.width = 800
        self.height = 600
        self.title = "SDL3 Example"

        self.renderer = POINTER(sdl3.SDL_Renderer)()
        self.window = POINTER(sdl3.SDL_Window)()

        if not sdl3.SDL_CreateWindowAndRenderer(
            "Hello World!".encode(),
            self.width, self.height, 0, self.window, self.renderer):
            sdl3.SDL_Log(f"Couldn't create window/renderer: {sdl3.SDL_GetError()}".encode())
            raise RuntimeError(f"SDL_CreateWindowAndRenderer failed: {sdl3.SDL_GetError()}")

        # self.create_window()
        # self.create_renderer()

        self.done = False

    def main(self) -> int:
        try:
            while not self.done:
                self.update()
                self.render()
                sdl3.SDL_Delay(c_uint32(16))
        finally:
            if self.renderer:
                sdl3.SDL_DestroyRenderer(self.renderer)
            if self.window:
                sdl3.SDL_DestroyWindow(self.window)
            sdl3.SDL_Quit()

        return 0

    def update(self) -> None:
        event = sdl3.SDL_Event()

        while sdl3.SDL_PollEvent(byref(event)):
            match event.type:
                # Handle different types of events
                case sdl3.SDL_EVENT_QUIT:
                    self.done = True

                case sdl3.SDL_EVENT_KEY_DOWN:
                    if event.key.key in [sdl3.SDLK_ESCAPE, sdl3.SDLK_Q]:
                       self.done = True


    def render(self) -> None:
        self.rgba_color(0, 0, 0, 1)
        sdl3.SDL_RenderClear(self.renderer)

        self.rgba_color(1, 0, 0, 1)

        step = 5
        center: tuple[float, float] = (self.width / 2.0, self.height / 2.0)
        for x in range(0, self.width, step):
           for y in range(0, self.height, step):
               self.line(*center, x, y)

        self.rgba_color(0, 1, 0, 1)
        self.rect(200, 150, 400, 300)

        sdl3.SDL_RenderPresent(self.renderer)

    def rgba_color(self, red: float, green: float, blue: float, alpha: float) -> bool:
        return bool(
            sdl3.SDL_SetRenderDrawColorFloat(self.renderer,
                c_float(red),
                c_float(green),
                c_float(blue),
                c_float(alpha)
            )
        )

    def line(self, x1: float, y1: float, x2: float, y2: float) -> bool:
        return bool(
            sdl3.SDL_RenderLine(self.renderer,
                c_float(x1),
                c_float(y1),
                c_float(x2),
                c_float(y2)
            )
        )

    def rect(self, x: float, y: float, w: float, h: float) -> bool:
        r = sdl3.SDL_FRect(
                c_float(x),
                c_float(y),
                c_float(w),
                c_float(h)
            )
        return bool(sdl3.SDL_RenderFillRect( self.renderer, byref(r)))

@sdl3.SDL_main_func
def main(argc: c_int, argv: sdl3.LP_c_char_p) -> int:
    return SDL3ExampleApp().main()

# EOF

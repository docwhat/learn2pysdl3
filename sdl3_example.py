import ctypes
from ctypes import c_char_p, c_int, c_uint32, c_float
import sdl3

class SDL3ExampleApp:
    height: int
    width: int

    window: sdl3.LP_SDL_Window
    renderer: sdl3.LP_SDL_Renderer

    # Initialize the window, renderers, etc.
    def __init__(self) -> None:
        if not sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO | sdl3.SDL_INIT_EVENTS): # pyright: ignore [reportArgumentType]
            raise RuntimeError(f"SDL_Init failed: {sdl3.SDL_GetError()}")

        self.width = 800
        self.height = 600

        self.window = sdl3.SDL_CreateWindow(
            c_char_p("SDL3 Example".encode()),
            c_int(self.width),
            c_int(self.height),
            sdl3.SDL_WINDOW_RESIZABLE | sdl3.SDL_WINDOW_METAL # pyright: ignore [reportArgumentType]
        )

        self.renderer = sdl3.SDL_CreateRenderer(
            self.window,
            c_char_p("software".encode())
        )
        if not (self.renderer):
            raise RuntimeError(f"SDL_CreateRenderer failed: {sdl3.SDL_GetError()}")

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

        while sdl3.SDL_PollEvent(ctypes.byref(event)):
            match event.type:
                # Handle different types of events
                case sdl3.SDL_EVENT_QUIT:
                    self.done = True

                case sdl3.SDL_EVENT_KEY_DOWN:
                    if event.key.key in [sdl3.SDLK_ESCAPE]:
                       self.done = True


    def render(self) -> None:
        rgba_back: tuple[c_float, c_float, c_float, c_float] = (0,0,0, 1)

        sdl3.SDL_SetRenderDrawColorFloat(self.renderer, *rgba_back)
        sdl3.SDL_RenderClear(self.renderer)

        rgba_front: tuple[c_float, c_float, c_float, c_float] = (1 ,0,0, 1)
        sdl3.SDL_SetRenderDrawColorFloat(self.renderer, *rgba_front)

        step = 5
        center: tuple[float, float] = (self.width / 2.0, self.height / 2.0)
        for x in range(0, self.width, step):
           for y in range(0, self.height, step):
               sdl3.SDL_RenderLine(self.renderer,
                   *[c_float(q) for q in center],
                   c_float(x), c_float(y))

        frect1 = sdl3.SDL_FRect()
        frect1.x = 200.0
        frect1.y = 150.0
        frect1.w = 400.0
        frect1.h = 300.0

        sdl3.SDL_RenderFillRect(self.renderer, ctypes.byref(frect1))

        sdl3.SDL_RenderPresent(self.renderer)

@sdl3.SDL_main_func
def main(argc: c_int, argv: sdl3.LP_c_char_p) -> int:
    return SDL3ExampleApp().main()

# EOF
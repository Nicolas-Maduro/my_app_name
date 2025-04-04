import asyncio
import reflex as rx

from rxconfig import config


class State(rx.State):
    segundos_restantes: int = 60
    esta_activo: bool = False
    valenciano_activo: bool = False
    
    @rx.event(background=True)
    async def iniciar_cuenta_regresiva(self):
        async with self:
            self.esta_activo = True
        while True:
            async with self:
                if not self.esta_activo or self.segundos_restantes <= 0:
                        return
                self.segundos_restantes -= 1
            await asyncio.sleep(1)
    
    @rx.event 
    def set_time(self, seconds: int):
        self.segundos_restantes = seconds

    @rx.event
    def detener(self):
        self.esta_activo = False

    @rx.event
    def reiniciar(self):
        self.segundos_restantes = 60
        self.esta_activo = False
    

    @rx.var
    def format_time(self) -> str:
        minutos = self.segundos_restantes // 60
        segundos = self.segundos_restantes % 60
        return f"{minutos}:{segundos:02d}"
   
       

def index() -> rx.Component:
    return rx.vstack(
            rx.heading("OLIMPIADA DE DEBATE 2025", size = "9"),
            rx.hstack(
                rx.button("Exposición", on_click=State.set_time(180), color_scheme= "red", size = "4"),
                rx.button("Refutacion 1", on_click=State.set_time(240), color_scheme= "red", size = "4"),
                rx.button("Refutacion 2", on_click=State.set_time(240), color_scheme= "red", size = "4"),
                rx.button("Conclusión", on_click=State.set_time(180), color_scheme= "red", size = "4"),
            ),
            rx.heading(State.format_time, font_size = "110px"),
            rx.hstack(
                rx.button("Iniciar", on_click=State.iniciar_cuenta_regresiva, color_scheme= "red", size = "4"),
                rx.button("Detener", on_click=State.detener, color_scheme= "red", size = "4"),
                rx.button("Reiniciar", on_click=State.reiniciar, color_scheme= "red", size = "4"),
            ),
            rx.hstack(
                rx.image(src="https://aulaelchesja.salesianos.edu/pluginfile.php/2/course/section/29/ELCHEcoleSJAVN3%20%281%29.jpg", width="300px", height="auto"),
                rx.image(src="https://salesianos.info/somosfuturo/wp-content/uploads/sites/12/2024/06/somos-futuro-principal.png", width="300px", height="auto"),
                spacing = "9",
            ),
            align="center",
            spacing= "9",
            height = "100vh",
            justify="center",
        )

app = rx.App()
app.add_page(index)

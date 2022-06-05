# w == escape
# | == carriage return
from types import LambdaType
from typing import Callable
from serialdevice import SerialDevice

# \x1b == ESC
C: Callable[[str], str] = lambda command: f"\x1b{command}\r"


class ExtronSerial(SerialDevice):
    ERRORS = {
        "E01": "Invalid input number",
        "E06": "Invalid switch attempt in this mode",
        "E10": "Invalid command",
        "E11": "Invalid preset number",
        "E12": "Invalid port number",
        "E13": "Invalid parameter",
        "E14": "Not valid for this configuration",
        "E17": "Invalid command for signal type",
        "E22": "Busy",
    }

    EDIDS = {
        "automatic": 0,
        "1280x800": 14,
        "720p60": 34,
        "1080p60": 45,
    }

    # w == escape
    # | == carriage return

    def __init__(self) -> None:
        serial_port = "/dev/serial/by-id/usb-Extron_Product-if00"
        baudrate = 9600
        super().__init__(serial_port, baudrate)

    def send_command(self, command: str, verbose: bool = False) -> str:
        response = super().send_command(command, verbose)

        if response[0] == "E":
            print(response, self.ERRORS.get(response, "Unknown"))

        return response

    def sleep(self) -> None:
        self.send_command(C("1PSAV"))

    def wake(self) -> None:
        self.send_command(C("0PSAV"))

    def change_input(self, input: int) -> None:
        self.send_command(f"{input}!")

    def is_sleeping(self) -> bool:
        response = self.send_command(C("PSAV"))

        return bool(int(response))

    def volume_up(self) -> int:
        volume = self.send_command("+V")
        return int(volume[3:])

    def volume_down(self) -> int:
        volume = self.send_command("-V")
        return int(volume[3:])

    def current_volume(self) -> int:
        return int(self.send_command("V"))

    def menu_toggle(self) -> None:
        self.send_command(C("MMENU"))

    def menu_enter(self) -> None:
        self.send_command(C("EMENU"))

    def menu_up(self) -> None:
        self.send_command(C("UMENU"))

    def menu_down(self) -> None:
        self.send_command(C("DMENU"))

    def menu_left(self) -> None:
        self.send_command(C("LMENU"))

    def menu_right(self) -> None:
        self.send_command(C("RMENU"))
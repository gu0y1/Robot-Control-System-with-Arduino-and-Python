import serial
import keyboard
import threading
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.style import Style
#以下适用于Windows系统
import os
print(0)
os.system('cls')


print(" ┌─Locomotion Control Panel───────────────────────────────────────────────────────┐")

def create_custom_progress_bar(value, max_value, bar_length):
    full_block = "█"
    empty_block = "▒"
    middle_block = "┃"
    middle_block_check = "▪"

    # 样式定义
    full_block_style = Style(color="dark_orange" if value < 0 else "blue", bgcolor=None)
    middle_block_style = Style(color="black", bgcolor="white") if value == 0 else Style()

    # 将值规范化到进度条长度的一半
    normalized_value = int((bar_length // 2) * abs(value) / max_value)

    if value < 0 and value >= - max_value:
        # 负数值：在左边填充█，右边填充▒
        bar = Text("  ")
        bar += Text(empty_block * (bar_length // 2 - normalized_value))
        bar += Text(full_block * normalized_value, style=full_block_style)
        bar += Text(middle_block, style=middle_block_style)
        bar += Text(empty_block * (bar_length // 2))
        bar += Text("  ")
    elif value == 0:
        bar = Text("  ")
        bar += Text(empty_block * (bar_length // 2))
        bar += Text(middle_block_check, style=middle_block_style)
        bar += Text(empty_block * (bar_length // 2))   
        bar += Text("  ")     
    elif value > 0 and value <= max_value:
        # 正数值：左边填充▒，右边填充█
        bar = Text("  ")
        bar += Text(empty_block * (bar_length // 2))
        bar += Text(middle_block, style=middle_block_style)
        bar += Text(full_block * normalized_value, style=full_block_style)
        bar += Text(empty_block * (bar_length // 2 - normalized_value))
        bar += Text("  ")
    elif value > max_value:
        bar = Text("  ")
        bar += Text(empty_block * (bar_length // 2))
        bar += Text(middle_block, style=middle_block_style)
        bar += Text(full_block * (bar_length // 2), style=full_block_style)
        bar += Text(" ▶")
    elif value < -max_value:
        bar = Text("◀ ")
        bar += Text(full_block * (bar_length // 2), style=full_block_style)
        bar += Text(middle_block, style=middle_block_style)
        bar += Text(empty_block * (bar_length // 2))
        bar += Text("  ")
    return bar

def format_number(number):
    return f"{number: >8}"

def format_number_right(number):
    return f"{number: <8}"

def read_from_arduino(live, arduino):
    while True:
        arduino.flushInput()
        data = arduino.readline().decode().strip()
        if data:
            parts = data.split(',')
            if len(parts) == 8:
                lastcommand, left_speed, right_speed, speed, acceleration, rotation, distance, checksum = parts
                checksum_valid = "OK! " if (float(speed) + float(acceleration) + float(rotation)) % 2 == float(checksum) else "ERR!"
                
                formatted_left_speed = format_number(left_speed)
                formatted_right_speed = format_number_right(right_speed)
                formatted_speed = format_number(speed)
                formatted_acceleration = format_number(acceleration)
                formatted_rotation = format_number(rotation)
                formatted_distance = format_number(distance)
                formatted_checksum = format_number(checksum)

                left_speed_bar = create_custom_progress_bar(float(left_speed), 100, 22)
                right_speed_bar = create_custom_progress_bar(float(right_speed), 100, 22)
                speed_bar = create_custom_progress_bar(float(speed), 400, 50)
                acceleration_bar = create_custom_progress_bar(float(acceleration), 10, 50)
                rotation_bar = create_custom_progress_bar(float(rotation), 90, 50)
                distance_bar = create_custom_progress_bar(float(distance), 100, 50)

                display_text = Text(f""" │                                                                                │
 │ Command：          [{lastcommand}]              ┏ {formatted_left_speed}    0    {formatted_right_speed} ┓              │
 │ Encoder:               {left_speed_bar}┃{right_speed_bar} │
 │ Speed:        {formatted_speed} {speed_bar} │
 │ Acceleration：{formatted_acceleration} {acceleration_bar} │
 │ Rotation:     {formatted_rotation} {rotation_bar} │
 │ Distance:     {formatted_distance} {distance_bar} │
 │ Parity Check: {formatted_checksum}, Status: {checksum_valid}                                           │
 │                                                                                │
 └────────────────────────────────────────────────────────────────────────────────┘""")

                live.update(display_text)


def main():
    console = Console()
    try:
        arduino = serial.Serial(port='COM4', baudrate=115200, timeout=2)
        live_text = Text(" │  _   _   _    _    _____     ______    _____   ______                          │\n │ | \\ | | | |  | |  / ____|   |  ____|  / ____| |  ____|                         │ \n │ |  \\| | | |  | | | (___     | |__    | |      | |__                            │ \n │ | . ` | | |  | |  \\___ \\    |  __|   | |      |  __|                           │ \n │ | |\\  | | |__| |  ____) |   | |____  | |____  | |____                          │ \n │ |_| \\_|  \\____/  |_____/    |______|  \\_____| |______|                         │ \n │ Retriving from UART...                                                         │ ")
        
        with Live(live_text, console=console, refresh_per_second=10
                  ) as live:
            thread = threading.Thread(target=read_from_arduino, args=(live, arduino))
            thread.daemon = True
            thread.start()

            while True:
                if keyboard.is_pressed('w'):
                    arduino.write(b'w')
                elif keyboard.is_pressed('s'):
                    arduino.write(b's')
                elif keyboard.is_pressed('a'):
                    arduino.write(b'a')
                elif keyboard.is_pressed('d'):
                    arduino.write(b'd')

    except Exception as e:
        console.print(f"[bold red]发生错误: {e}[/bold red]")

if __name__ == '__main__':
    main()

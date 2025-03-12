import serial
import asyncio

radicals_left = ["氵", "扌", "亻", "讠", "木"]
radicals_right = ["白", "目", "土", "可", "每", "台", "工", "木"]

# 1 2
# 3 4

configuration = {
    (1, 1, 0, 0): "氵",
    (1, 0, 1, 0): "木",
    (1, 0, 0, 1): "讠",
    (0, 1, 1, 0): "亻",
    (0, 1, 0, 1): "扌",
    (0, 0, 1, 1): "白",
    # (0, 1, 1, 1): "目",
    (1, 0, 1, 1): "土",
    (1, 1, 0, 1): "可",
    (1, 1, 1, 0): "每",
    (0, 1, 1, 1): "台",
    (1, 1, 1, 1): "工"
}

valid_characters = {
    ("氵", "白"): "泊",
    ("氵", "木"): "沐",
    ("氵", "可"): "河",
    ("氵", "每"): "海",
    ("氵", "台"): "治",
    ("氵", "工"): "江",

    ("扌", "白"): "拍",
    ("扌", "可"): "抲",
    ("扌", "台"): "抬",
    ("扌", "每"): "挴",
    ("扌", "工"): "扛",

    ("亻", "木"): "休",
    ("亻", "白"): "伯",
    ("亻", "可"): "何",
    ("亻", "台"): "佁",
    ("亻", "每"): "侮",
    ("亻", "工"): "仜",

    ("讠", "可"): "诃",
    ("讠", "每"): "诲",
    ("讠", "台"): "诒",
    ("讠", "工"): "讧",

    ("木", "白"): "柏",
    ("木", "木"): "林",
    ("木", "可"): "柯",
    ("木", "每"): "梅",
    ("木", "台"): "枱",
    ("木", "工"): "杠"
}


class RadicalTileGame:
    def __init__(self):
        self.current_left_radical = None
        self.current_right_radical = None
        self.last_detected_config = None

    def process_sensor_input(self, sensor_values, is_left):
        """
        Process the sensor input from the 4 spots on the electric board.

        Args:
            sensor_values: A list or tuple of 4 booleans (0 or 1) indicating which spots are connected
                          [spot1, spot2, spot3, spot4]

        Returns:
            Detected radical or None if the configuration is not recognized
        """
        # Convert sensor values to a tuple for dictionary lookup
        sensor_config = tuple(sensor_values)

        # Check if the configuration is valid
        if sensor_config in configuration:
            detected_radical = configuration[sensor_config]
            self.update_current_radicals(detected_radical, is_left)
            self.last_detected_config = sensor_config
            return detected_radical
        else:
            print(f"Unknown configuration ({'L' if is_left else 'R'}): {sensor_config}")
            return None

    def update_current_radicals(self, detected_radical, is_left):
        """Update the current left or right radical based on the detected radical."""
        if is_left:
            self.current_left_radical = detected_radical
            print(f"Left radical set to: {detected_radical}")
        else:
            self.current_right_radical = detected_radical
            print(f"Right radical set to: {detected_radical}")

        # Check if we can form a valid character
        self.check_valid_character()

    def check_valid_character(self):
        """Check if the current left and right radicals form a valid character."""
        if self.current_left_radical and self.current_right_radical:
            radical_pair = (self.current_left_radical,
                            self.current_right_radical)
            if radical_pair in valid_characters:
                character = valid_characters[radical_pair]
                print(f"Valid character formed: {character}")
                print(
                    f"{self.current_left_radical} + {self.current_right_radical} = {character}")
                return character
            else:
                print(
                    f"Invalid combination: {self.current_left_radical} + {self.current_right_radical}")
                return None
        return None

    def reset(self):
        """Reset the current radical selections."""
        self.current_left_radical = None
        self.current_right_radical = None
        print("Game reset. Place new radicals on the board.")

# Main function for testing

async def run(game):
    ser = serial.Serial('/dev/cu.usbmodem1101', 115200, timeout=0.1) # COM port, Baudrate, 1/timeout is the frequency at which the port is read
        
    while True:
        data = ser.readline().decode().strip()
        if data:
            data = int(data)
            # print(data)
            left_data = (
                (data & (1 << 7)) >> 7,
                (data & (1 << 6)) >> 6,
                (data & (1 << 5)) >> 5,
                (data & (1 << 4)) >> 4
            )
            right_data = (
                (data & (1 << 3)) >> 3,
                (data & (1 << 2)) >> 2,
                (data & (1 << 1)) >> 1,
                (data & (1 << 0)) >> 0
            )
            # print('left', left_data, 'right', right_data)

            detected_radical = game.process_sensor_input(
                tuple(left_data), True)
            if detected_radical:
                print(f"Detected radical: {detected_radical}")

            detected_radical = game.process_sensor_input(
                tuple(right_data), False)
            if detected_radical:
                print(f"Detected radical: {detected_radical}")

            print()
            await asyncio.sleep(0.4)

def main():
    game = RadicalTileGame()

    print("Chinese Radical Tile Game")
    print("-------------------------")
    print("Place radical tiles on the electric board to form Chinese characters.")

    # Test with some simulated sensor inputs
    # test_configs = [
    #     (1, 1, 0, 0),  # 氵 (water radical)
    #     (0, 0, 1, 1),  # 白 (white radical)
    #     (1, 0, 1, 0),  # 扌 (hand radical)
    #     (0, 1, 1, 1),  # 目 (eye radical)
    # ]

    # for config in test_configs:
    #     print("\nDetected configuration:", config)
    #     detected_radical = game.process_sensor_input(config)
    #     if detected_radical:
    #         print(f"Detected radical: {detected_radical}")

    # Turn this off to manually enter digits.
    DIGITAL_MODE = False

    # Interactive mode
    print("\nEntering interactive mode...")


    if DIGITAL_MODE:
        print("Enter 4 binary digits (0 or 1) separated by spaces, or 'q' to quit, 'r' to reset:")
        while True:
            user_input = input("> ").strip().lower()

            if user_input == 'q':
                break
            elif user_input == 'r':
                game.reset()
                continue

            if DIGITAL_MODE:
                try:
                    sensor_values = [int(val) for val in user_input.split()]
                    if len(sensor_values) == 4 and all(val in [0, 1] for val in sensor_values):
                        detected_radical = game.process_sensor_input(
                            tuple(sensor_values))
                        if detected_radical:
                            print(f"Detected radical: {detected_radical}")
                    else:
                        print("Invalid input. Enter exactly 4 binary digits (0 or 1).")
                except ValueError:
                    print("Invalid input. Enter binary digits separated by spaces.")
    else:
        ser = serial.Serial('/dev/cu.usbmodem1101', 115200, timeout=0.1) # COM port, Baudrate, 1/timeout is the frequency at which the port is read
        
        while True:
            data = ser.readline().decode().strip()
            if data:
                data = int(data)
                # print(data)
                left_data = (
                    (data & (1 << 7)) >> 7,
                    (data & (1 << 6)) >> 6,
                    (data & (1 << 5)) >> 5,
                    (data & (1 << 4)) >> 4
                )
                right_data = (
                    (data & (1 << 3)) >> 3,
                    (data & (1 << 2)) >> 2,
                    (data & (1 << 1)) >> 1,
                    (data & (1 << 0)) >> 0
                )
                # print('left', left_data, 'right', right_data)

                detected_radical = game.process_sensor_input(
                    tuple(left_data), True)
                if detected_radical:
                    print(f"Detected radical: {detected_radical}")

                detected_radical = game.process_sensor_input(
                    tuple(right_data), False)
                if detected_radical:
                    print(f"Detected radical: {detected_radical}")

                print()




if __name__ == "__main__":
    main()

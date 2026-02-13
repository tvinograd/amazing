from typing import Any


class ConfigParser:
    "Configuration file parser for maze generation."

    required_keys: set[str] = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
    }

    @staticmethod
    def parse_coordinates(value: str) -> tuple[int, int]:
        """Parse 'x,y' string into a tuple of two integers."""
        parts = value.split(",")
        if len(parts) != 2:
            raise ValueError
        return (int(parts[0].strip()), int(parts[1].strip()))

    def convert_values(self, raw: dict[str, str]) -> dict[str, Any]:
        """Convert raw string values to appropriate types."""
        config: dict[str, Any] = {}

        # Height/width -> int
        try:
            config["WIDTH"] = int(raw["WIDTH"])
            config["HEIGHT"] = int(raw["HEIGHT"])
        except ValueError:
            print("Error: WIDTH and HEIGHT must be integers.")
            return {}

        # Entry/exit -> int tuple
        try:
            config["ENTRY"] = self.parse_coordinates(raw["ENTRY"])
            config["EXIT"] = self.parse_coordinates(raw["EXIT"])
            if config["ENTRY"] == config["EXIT"]:
                print("Error: ENTRY and EXIT must be different.")
                return {}
        except ValueError:
            print("Error: ENTRY and EXIT must be in format 'x,y' with "
                  "integers.")
            return {}

        # Perfect -> bool
        if raw["PERFECT"].lower() not in ("true", "false"):
            print("Error: PERFECT must be 'True' or 'False'.")
            return {}
        config["PERFECT"] = raw["PERFECT"].lower() == "true"

        # Output file name -> str
        config["OUTPUT_FILE"] = raw["OUTPUT_FILE"]

        # Seed -> int | None
        if raw.get("SEED"):
            try:
                config["SEED"] = int(raw["SEED"])
            except ValueError:
                config["SEED"] = None
        else:
            config["SEED"] = None

        return config

    def parse_config(self, filepath: str) -> dict[str, Any]:
        """Parse a maze configuration file."""

        # Read file
        try:
            with open(filepath, "r") as file:
                lines = file.readlines()
        except OSError as e:
            print(f"Error: {e}")
            return {}

        # Parse KEY=VALUE pairs
        raw: dict[str, str] = {}
        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" not in stripped:
                print(f"Error: Invalid syntax on line {line_num}: "
                      f"'{stripped}')")
                return {}

            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                print(f"Error: Missing key on line {line_num}.")
                return {}

            raw[key] = value

        # Check required keys
        missing = self.required_keys - raw.keys()
        if missing:
            print(f"Error: Missing required keys: {', '.join(missing)}")
            return {}

        # Convert types and return
        return self.convert_values(raw)


if __name__ == "__main__":
    config = ConfigParser().parse_config("config.txt")
    if config:
        print("Configuration file parsing is successful:")
        for key, value in config.items():
            print(f"  {key}: {value} ({type(value).__name__})")
    else:
        print("Configuration file parsing failed.")

#!/usr/bin/env python3
"""
Password Manager (CLI) - combines CLI args + config file + auto-save passwords.
Save this as `password_manager.py`.
"""

import argparse
import json
import os
import secrets
import random
import string
import datetime
from pathlib import Path

# ----- defaults -----
DEFAULT_CONFIG = {
    "length": 12,
    "use_uppercase": True,
    "use_numbers": True,
    "use_special_chars": True,
    "output_file": "passwords.txt"
}
CONFIG_PATH = "config.json"

# ----- config helpers -----
def load_config(path: str = CONFIG_PATH) -> dict:
    p = Path(path)
    if p.exists():
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
            # Merge with defaults to ensure fields exist
            cfg = {**DEFAULT_CONFIG, **data}
            return cfg
        except Exception as e:
            print(f"[WARNING] Failed to read {path}: {e}. Using defaults.")
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(cfg: dict, path: str = CONFIG_PATH) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
        print(f"[INFO] Config saved to {path}")
    except Exception as e:
        print(f"[ERROR] Could not save config: {e}")

# ----- password generation -----
def generate_password(length: int = 12,
                      use_uppercase: bool = True,
                      use_numbers: bool = True,
                      use_special_chars: bool = True) -> str:
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase if use_uppercase else ""
    numbers = string.digits if use_numbers else ""
    special_chars = string.punctuation if use_special_chars else ""

    all_chars = lowercase + uppercase + numbers + special_chars
    if not all_chars:
        raise ValueError("No character sets selected. Enable at least one category.")

    # Required characters to ensure at least one of each selected category.
    required = []
    if use_uppercase:
        required.append(secrets.choice(uppercase))
    if use_numbers:
        required.append(secrets.choice(numbers))
    if use_special_chars:
        required.append(secrets.choice(special_chars))

    if length < len(required):
        raise ValueError(f"Password length {length} too small for the selected options. "
                         f"Increase length to at least {len(required)}.")

    # Fill remaining using secure randomness
    remaining = [secrets.choice(all_chars) for _ in range(length - len(required))]
    pwd_list = required + remaining

    # Shuffle using SystemRandom for better randomness
    sr = random.SystemRandom()
    sr.shuffle(pwd_list)

    return "".join(pwd_list)

# ----- file append helper -----
def append_to_file(output_file: str, password: str, annotate: bool = True) -> None:
    p = Path(output_file)
    try:
        with p.open("a", encoding="utf-8") as f:
            if annotate:
                f.write(f"{datetime.datetime.now().isoformat()}    {password}\n")
            else:
                f.write(password + "\n")
    except Exception as e:
        print(f"[ERROR] Could not write to {output_file}: {e}")

# ----- main CLI -----
def main():
    parser = argparse.ArgumentParser(description="Random Password Generator + Config + Auto-save")
    parser.add_argument("-l", "--length", type=int, help="Password length (overrides config)")
    parser.add_argument("-u", "--no-uppercase", action="store_true", help="Exclude uppercase letters")
    parser.add_argument("-n", "--no-numbers", action="store_true", help="Exclude numbers")
    parser.add_argument("-s", "--no-special", action="store_true", help="Exclude special characters")
    parser.add_argument("-o", "--output", type=str, help="Output filename (overrides config)")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of passwords to generate (default: 1)")
    parser.add_argument("--save-config", action="store_true", help="Save the current options into config.json")
    parser.add_argument("--show-config", action="store_true", help="Show the loaded config and exit")
    parser.add_argument("--no-save", action="store_true", help="Do NOT save generated password(s) to the output file")
    args = parser.parse_args()

    # Load config and apply CLI overrides
    cfg = load_config(CONFIG_PATH)

    # override with CLI if provided
    if args.length is not None:
        cfg["length"] = args.length

    cfg["use_uppercase"] = False if args.no_uppercase else cfg.get("use_uppercase", True)
    cfg["use_numbers"] = False if args.no_numbers else cfg.get("use_numbers", True)
    cfg["use_special_chars"] = False if args.no_special else cfg.get("use_special_chars", True)

    if args.output:
        cfg["output_file"] = args.output

    if args.show_config:
        print("Loaded configuration:")
        print(json.dumps(cfg, indent=4))
        return

    if args.save_config:
        save_config(cfg, CONFIG_PATH)

    # Validate at least one char set
    if not (cfg["use_uppercase"] or cfg["use_numbers"] or cfg["use_special_chars"] or True):
        # lowercase is always available, so this line won't happen; leaving for completeness
        print("[ERROR] No character sets selected.")
        return

    # Generate passwords
    for i in range(args.count):
        try:
            pwd = generate_password(
                length=cfg["length"],
                use_uppercase=cfg["use_uppercase"],
                use_numbers=cfg["use_numbers"],
                use_special_chars=cfg["use_special_chars"]
            )
        except ValueError as e:
            print(f"[ERROR] {e}")
            return

        print(f"Generated Password [{i+1}]: {pwd}")

        if not args.no_save:
            append_to_file(cfg["output_file"], pwd)
            print(f"[INFO] Saved to {cfg['output_file']}")

if __name__ == "__main__":
    main()

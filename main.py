import os
from platform import system


def start_atm():
    clear_screen()

    print("Welcome")
    print("-------")
    print("1) Customer")
    print("2) Admin")

    print("\nPlease select an option.")
    try:
        selection = get_user_selection(["1", "2"])
    except ValueError:
        # Return to start
        return
    if selection == "2":
        clear_screen()
        print("Admin Menu")
    else:
        clear_screen()
        print("Main Menu")

def get_user_selection(options):
    """Get user input and check against a list of valid options.

    Args:
        options (list): List of valid input options.

    Raises:
        ValueError: If the input doesn't match any of the options.

    Returns:
        user_input (str): One of the valid options from the user.
    """
    user_input = input("-> ")
    if user_input not in options:
        raise ValueError("Invalid option")
    return user_input



def clear_screen():
    """Clear the terminal screen on Windows, Linux and Mac.

    Raises:
        RuntimeError: If system type is not supported.
    """
    system_type = system()
    if system_type == "Windows":
        os.system("cls")
    elif system_type in ["Linux", "Darwin"]:
        os.system("clear")
    else:
        raise RuntimeError("Incompatible system")


if __name__ == "__main__":
    # while True:
    start_atm()
